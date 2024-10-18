from flask import render_template, request, redirect, url_for, session
from app import app, db
from app.models.tables import Materias
import fitz  # PyMuPDF
import re
import os
import uuid



def process_pdf(file_path):
    """Extrai o texto do PDF e retorna as matérias cursadas."""
    # Abrir o PDF
    pdf_reader = fitz.open(file_path)
    extracted_text = ""

    # Extrair texto de todas as páginas do PDF
    for page in pdf_reader:
        extracted_text += page.get_text()

   pattern = re.compile(r'(CTIA\d{2}|CTIB\d{2})\s+.*?\s+(AP|RR|RF|TR)', re.DOTALL)
    ap_matches = pattern.findall(extracted_text)
    
    matches = []
    for match in ap_matches:
        cod, status = match
        if status == 'AP':
            matches.append(cod)

    materias_cursadas = Materias.query.filter(Materias.codigo.in_(matches)).all()

    resultado = [(materia.codigo, materia.nome,materia.natureza) for materia in materias_cursadas]
    return resultado

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/cursadas", methods=['GET', 'POST'])
def cursadas():
    if request.method == 'POST':
        pdf_file = request.files['pdf']
        if pdf_file:
            session_id = str(uuid.uuid4())
            session['pdf_file'] = session_id
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.pdf")
            pdf_file.save(file_path)
            return redirect(url_for('cursadas'))

    session_id = session.get('pdf_file')
    if not session_id:
        return render_template("cursadas.html", materias_cursadas=None)

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.pdf")
    if not os.path.exists(file_path):
        return render_template("cursadas.html", materias_cursadas=None)

    materias_cursadas = process_pdf(file_path)
    return render_template("cursadas.html", materias_cursadas=materias_cursadas)

@app.route("/todas", methods=['GET'])
def todas():
    materias = Materias.query.all()
    return render_template("materias.html", materias=materias)

@app.route("/previsao", methods=['GET'])
def previsao():
    session_id = session.get('pdf_file')
    if not session_id:
        return redirect(url_for('index'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.pdf")
    if not os.path.exists(file_path):
        return redirect(url_for('index'))

    materias_cursadas = process_pdf(file_path)


    

    # Consultar as views no banco de dados
    cienciadedados = db.session.execute(db.text("SELECT * FROM cienciadedados")).fetchall()
    estudodeengenharia = db.session.execute(db.text("SELECT * FROM estudodeengenharia")).fetchall() 
    engenhariadeprod = db.session.execute(db.text("SELECT * FROM engenhariadeprod")).fetchall()
    b_i = db.session.execute(db.text("SELECT * FROM b_i")).fetchall()
   

    return render_template("previsao.html", 
                           cienciadedados=cienciadedados, 
                           estudodeengenharia=estudodeengenharia, 
                           engenhariadeprod=engenhariadeprod, 
                           b_i=b_i,
                           materias_cursadas=materias_cursadas)
