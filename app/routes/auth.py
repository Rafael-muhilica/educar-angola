from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User
import re

auth = Blueprint('auth', __name__, template_folder='../templates')

def valid_username_rules(username: str) -> tuple[bool, str]:
    if not username or len(username) < 3:
        return False, "O nome de usuário deve ter pelo menos 3 caracteres."
    # Verifica se há letras maiúsculas
    if any(ch.isalpha() and ch.isupper() for ch in username):
        return False, "O nome de usuário deve estar em letras minúsculas."
    # Verifica se tem pelo menos 1 carácter especial (não alfanumérico)
    if not re.search(r'[^a-z0-9]', username):
        return False, "O nome de usuário deve conter pelo menos 1 caractere especial (ex: @, ., -, _)."
    return True, ""

@auth.route('/')
def inicio():
    return render_template('inicio.html')
@auth.route('/sobre')
def sobre():
    return render_template('sobre.html')
@auth.route('/contato')
def contato():
    return render_template('contato.html')
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip().lower()
        nome_usuario = request.form.get('nome_usuario', '').strip()
        senha = request.form.get('senha', '')
        genero = request.form.get('genero', '').strip()
        confirmar_senha = request.form.get('confirmar_senha', '')

        if not nome or not email or not nome_usuario or not senha or not confirmar_senha:
            flash('Preencha os campos obrigatórios.', 'error')
            return render_template('register.html', nome = nome, email = email, nome_usuario = nome_usuario, senha = senha, genero = genero, confirmar_senha = confirmar_senha)
        if senha != confirmar_senha:
            flash(" As senhas não coincidem.")
            return ("register.html")

        ok, msg = valid_username_rules(nome_usuario)
        if not ok:
            flash(msg, 'error')
            return render_template('register.html')

        if User.query.filter((User.email == email) | (User.nome_usuario == nome_usuario)).first():
            flash('Email ou nome de usuário já existente.', 'error')
            return render_template('register.html')

        user = User(nome=nome, email=email, nome_usuario=nome_usuario, genero=genero)
        user.set_password(senha)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')
@auth.route("/perfil")
def perfil():
    return render_template("perfil.html")
@auth.route("/curso")
def cursos():
    return render_template("curso.html")
@auth.route("/certificado")
def certificados():
    return render_template("certificados.html")
@auth.route("/perfil")
def editar_perfil():
    return render_template("perfil.html")
@auth.route("/curso")
def lista_curso():
    return render_template("perfil.html")
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome_usuario = request.form.get('nome_usuario', '').strip()
        senha = request.form.get('senha', '')

        user = User.query.filter_by(nome_usuario=nome_usuario).first()
        if not user or not user.check_password(senha):
            flash('Credenciais inválidas.', 'error')
            return render_template('login.html')

        session['user_id'] = user.id
        flash('Bem-vindo!', 'success')
        return redirect(url_for('auth.dashboard'))

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você saiu da sessão.', 'info')
    return redirect(url_for('auth.inicio'))

@auth.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Você precisa fazer login primeiro.", "error")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('auth.login'))

    return render_template('dashboard.html', user=user)
