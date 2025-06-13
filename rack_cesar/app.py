from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#  static_folder="rack_cesar/static", template_folder="templates"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Aluno(db.Model):
    __tablename__ = 'alunos'
    cpf = db.Column(db.String(14), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    alunos = Aluno.query.all()
    return render_template('login.html', alunos=alunos)


@app.route('/cadastro', methods=['GET'])
def exibir_cadastro():
    # Renderiza o template 'cadastro.html'.
    return render_template('cadastro.html')

# Rota para cadastrar um aluno. Aceita apenas o método POST (quando o formulário é enviado).


@app.route('/cadastro', methods=['POST'])
def cadastrar():
    # Obtém os dados dos campos do formulário enviados via POST.
    cpf = request.form.get('cpf')
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')

    # Verifica se todos os campos obrigatórios foram preenchidos.
    if not cpf or not nome or not email or not telefone:
        # Retorna uma mensagem de erro com status 400 (Bad Request) se algum campo estiver vazio.
        return "Erro: Todos os campos devem ser preenchidos!", 400

    # Verifica se o CPF já existe no banco de dados para evitar duplicidades.
    if Aluno.query.filter_by(cpf=cpf).first():
        # Retorna uma mensagem de erro com status 400 se o CPF já estiver cadastrado.
        return "Erro: CPF já cadastrado!", 400

    # Cria uma nova instância de Aluno com os dados recebidos do formulário.
    novo_aluno = Aluno(cpf=cpf, nome=nome, email=email, telefone=telefone)
    # Adiciona o novo objeto Aluno à sessão do banco de dados.
    db.session.add(novo_aluno)
    # Confirma as alterações no banco de dados (salva o novo aluno).
    db.session.commit()

    # Redireciona o usuário para a página de login após o cadastro bem-sucedido.
    return redirect(url_for('login'))


# Bloco principal que executa o servidor Flask.
if __name__ == '__main__':
    # Inicia o servidor em modo de depuração (debug=True), o que permite:
    # 1. Recarregamento automático do servidor ao detectar mudanças no código.
    # 2. Exibição de informações detalhadas de erro no navegador.
    app.run(debug=True)
