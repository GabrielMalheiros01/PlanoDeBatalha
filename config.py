from app import app
import os

SQLALCHEMY_DATABASE_URI = 'postgresql://guerreiros:LVh6RmcMGQzlemZYZbod5aOfgUsaikZF@dpg-cqv4mj3v2p9s73ec2vjg-a.oregon-postgres.render.com/bdmaterias'
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = 'uploads'
SECRET_KEY = os.getenv('SECRET_KEY', 'secreta')