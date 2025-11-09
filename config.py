import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'esta_chave_é_muito_segura_e_secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///banco.db' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
