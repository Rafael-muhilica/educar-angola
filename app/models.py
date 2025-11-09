from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(250), nullable=False)
    nome_usuario = db.Column(db.String(250), nullable=False, unique=True, index=True)
    genero = db.Column(db.String(30), nullable=True)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, senha: str):
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f'<User {self.nome_usuario} ({self.email})>'


