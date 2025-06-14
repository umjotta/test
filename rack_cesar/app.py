from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# Adicionado para criptografar senhas
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Aluno(db.Model):
    __tablename__ = 'alunos'
    cpf = db.Column(db.String(14), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    # Alterado: agora armazena a senha criptografada
    senha_hash = db.Column(db.String(255), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Alterado: agora verifica se a requisição é POST para processar login
        cpf = request.form.get('cpf')
        senha = request.form.get('senha')

        aluno = Aluno.query.filter_by(cpf=cpf).first()
        # Alterado: verifica a senha criptografada
        if aluno and check_password_hash(aluno.senha_hash, senha):
            # Alterado: redireciona para a página home.html
            return redirect(url_for('home'))
        else:
            return "Erro: CPF ou senha incorretos!", 400

    return render_template('login.html')


@app.route('/home')  # Alterado: Criada a rota para exibir home.html
def home():
    return render_template('home.html')


@app.route('/cadastro', methods=['GET'])
def exibir_cadastro():
    return render_template('cadastro.html')


@app.route('/cadastro', methods=['POST'])
def cadastrar():
    cpf = request.form.get('cpf')
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    # Alterado: agora captura a senha do formulário
    senha = request.form.get('senha')

    if not cpf or not nome or not email or not telefone or not senha:
        return "Erro: Todos os campos devem ser preenchidos!", 400

    if Aluno.query.filter_by(cpf=cpf).first():
        return "Erro: CPF já cadastrado!", 400

    # Alterado: agora criptografa a senha antes de salvar
    senha_hash = generate_password_hash(senha)

    novo_aluno = Aluno(cpf=cpf, nome=nome, email=email,
                       telefone=telefone, senha_hash=senha_hash)
    db.session.add(novo_aluno)
    db.session.commit()

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
