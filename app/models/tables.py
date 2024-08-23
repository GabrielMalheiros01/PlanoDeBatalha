from app import db

class Materias(db.Model):
    __tablename__ = 'materias'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    carga_horaria = db.Column(db.Integer, nullable=False)
    natureza = db.Column(db.String(2), nullable=False)


    def __init__(self, codigo, nome, carga_horaria, natureza):
        self.codigo = codigo
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.natureza = natureza
    def __repr__(self):
        return "<Materias %r>" % self.nome