from app import app, db
from flask import render_template, request
from app.models.tables import Materias
import fitz  # PyMuPDF
import re
import os
from werkzeug.utils import secure_filename

# Configurar um diretório para armazenar o arquivo PDF
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Certifique-se de que o diretório de uploads existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/cursadas", methods=['GET', 'POST'])
def cursadas():
    if request.method == 'POST':
        # Recebendo o arquivo PDF enviado
        pdf_file = request.files['pdf']
        
        # Gerar um nome de arquivo seguro e definir o caminho do arquivo
        filename = 'uploaded_pdf.pdf'  # Nome fixo para garantir substituição
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Salvar o arquivo PDF no caminho especificado (substituir o antigo)
        pdf_file.save(file_path)

        # Abrindo o PDF e extraindo texto
        pdf_reader = fitz.open(file_path)
        extracted_text = ""
        
        for page in pdf_reader:
            extracted_text += page.get_text()
        
        # Expressão regular para capturar somente os códigos das disciplinas
        pattern = re.compile(r'(CTIA\d{2})')
        matches = pattern.findall(extracted_text)
        
        # Lista para armazenar matérias encontradas
        materias_cursadas = []

        for codigo in matches:
            # Verifica se a matéria está no banco de dados usando o código
            materia = Materias.query.filter_by(codigo=codigo).first()
            if materia:
                materias_cursadas.append(materia)
        
        # Renderiza o template e passa as matérias encontradas
        return render_template("cursadas.html", materias_cursadas=materias_cursadas)

    # Caso não haja um PDF enviado via POST, renderize a página com a lista vazia
    return render_template("cursadas.html", materias_cursadas=None)

@app.route("/todas", methods=['GET'])
def todas():
    # Buscar todas as matérias do banco de dados
    materias = Materias.query.all()
    # Renderizar o template e passar as matérias para ele
    return render_template("materias.html", materias=materias)

@app.route("/previsao", methods=['GET'])
def previsao():
    # Caminho para o arquivo PDF já salvo anteriormente
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_pdf.pdf')
    
    # Abrindo o PDF e extraindo texto
    pdf_reader = fitz.open(file_path)
    extracted_text = ""
    for page in pdf_reader:
        extracted_text += page.get_text()
    
    # Expressão regular para capturar somente os códigos das disciplinas
    pattern = re.compile(r'(CTIA\d{2}|CTIB\d{2})')
    matches = pattern.findall(extracted_text)
    
    # Lista para armazenar matérias cursadas
    materias_cursadas = []
    for codigo in matches:
        # Verifica se a matéria está no banco de dados usando o código
        materia = Materias.query.filter_by(codigo=codigo).first()
        if materia:
            materias_cursadas.append(materia)
    
    # Buscar todas as matérias do banco de dados para categorização
    todas_materias = Materias.query.all()
    
    # Organizar matérias por categoria
    materias_cc = [m for m in todas_materias if m.codigo.startswith('CTIA') and 1 <= int(m.codigo[4:]) <= 50]
    materias_es = [m for m in todas_materias if m.codigo.startswith('CTIA') and 51 <= int(m.codigo[4:]) <= 99]
    materias_ep = [m for m in todas_materias if m.codigo.startswith('CTIB') and 1 <= int(m.codigo[4:]) <= 27]
    
    # Passar as listas de matérias e as matérias cursadas para o template
    return render_template("previsao.html", 
                           materias_cc=materias_cc, 
                           materias_es=materias_es, 
                           materias_ep=materias_ep, 
                           materias_cursadas=materias_cursadas)

