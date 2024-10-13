from app import app
import os

SQLALCHEMY_DATABASE_URI = 'postgresql://materias_bd_user:MmzGj7PCeTSNKLVMNvyRjIvPGMW9rwSQ@dpg-cs5vuf3tq21c73dnl8t0-a.oregon-postgres.render.com/materias_bd''
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = 'uploads'
SECRET_KEY = os.getenv('SECRET_KEY', 'secreta')
