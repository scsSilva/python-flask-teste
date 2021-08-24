from flask import render_template, request, Blueprint, url_for
from werkzeug.utils import redirect
from config import db
from model.usuario import Usuario

TEMPLATES = "./view"
STATIC = "./static"

usuario_blueprint = Blueprint('usuarios', __name__, template_folder=TEMPLATES, static_folder=STATIC)

@usuario_blueprint.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    nome = request.form.get('nome')
    email = request.form.get('email')

    usuarios = Usuario.query.all()
    for u in usuarios:
        if u.email == email:
            return 'Email já cadastrado!'

    usuario = Usuario(nome, email)
    db.session.add(usuario)
    db.session.commit()
    return 'Usuário cadastrado com sucesso!'

@usuario_blueprint.route('/consultarUsuarios')
def consultarUsuarios():
    usuarios = Usuario.query.all()
    return render_template('listarUsuarios.html', usuarios=usuarios)

@usuario_blueprint.route('/usuarios/form')
def abrirCadastroUsuario():
    return render_template('cadastrarUsuario.html')

@usuario_blueprint.route('/usuario/edit/<int:index>', methods=['GET', 'POST'])
def abrirEditarUsuario(index):
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        usuario = Usuario.query.filter_by(Usuario.id == index).first()
        usuario.nome = nome
        usuario.email = email
        db.session.commit()
        return redirect(url_for('usuario_blueprint.consultarUsuarios'))
    return render_template('editarUsuario.html', index=index)

@usuario_blueprint.route('/delete/<int:index>', methods=['POST', 'GET'])
def delete(index):
    Usuario.query.filter(Usuario.id == index).delete()
    return redirect(url_for('usuario_blueprint.consultarUsuarios'))