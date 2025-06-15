from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
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
    senha_hash = db.Column(db.String(255), nullable=False)


class Questao(db.Model):
    __tablename__ = 'questoes'
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(500), nullable=False)
    alternativa_a = db.Column(db.String(200), nullable=False)
    alternativa_b = db.Column(db.String(200), nullable=False)
    alternativa_c = db.Column(db.String(200), nullable=False)
    alternativa_d = db.Column(db.String(200), nullable=False)
    alternativa_e = db.Column(db.String(200), nullable=False)
    # Armazena 'A', 'B', 'C', etc.
    resposta_correta = db.Column(db.String(1), nullable=False)


class HistoricoResposta(db.Model):
    __tablename__ = 'historico_respostas'
    id = db.Column(db.Integer, primary_key=True)
    questao_id = db.Column(db.Integer, db.ForeignKey('questoes.id'))
    resposta_usuario = db.Column(db.String(1), nullable=False)
    acertou = db.Column(db.Boolean, nullable=False)


with app.app_context():
    db.create_all()


with app.app_context():
    questoes = [
        # Questões de Português
        Questao(texto="Qual é a figura de linguagem presente na frase: 'A cidade dorme tranquila sob o céu estrelado.'?",
                alternativa_a="Metáfora", alternativa_b="Hipérbole", alternativa_c="Personificação",
                alternativa_d="Paradoxo", alternativa_e="Eufemismo", resposta_correta="C"),

        Questao(texto="Qual é a função do pronome relativo na frase: 'O livro que comprei é muito interessante.'?",
                alternativa_a="Substituir um substantivo", alternativa_b="Indicar posse",
                alternativa_c="Introduzir uma oração subordinada", alternativa_d="Expressar um sentimento",
                alternativa_e="Enfatizar uma ideia",
                resposta_correta="C"),

        Questao(texto="O verbo 'caber' na primeira pessoa do singular do futuro do presente é:",
                alternativa_a="Caberei", alternativa_b="Cabo", alternativa_c="Cabei",
                alternativa_d="Caberia", alternativa_e="Cabeste",
                resposta_correta="A"),

        # Questões de Matemática
        Questao(texto="Se um número é multiplicado por 3 e depois somado a 5, o resultado é 20. Qual é o número?",
                alternativa_a="3", alternativa_b="5", alternativa_c="7", alternativa_d="6", alternativa_e="4",
                resposta_correta="C"),

        Questao(texto="O perímetro de um triângulo equilátero com lados de 12 cm é:",
                alternativa_a="24 cm", alternativa_b="30 cm", alternativa_c="36 cm", alternativa_d="48 cm",
                alternativa_e="12 cm",
                resposta_correta="C"),

        Questao(texto="Se um cilindro tem altura de 10 cm e raio da base de 5 cm, qual é o seu volume?",
                alternativa_a="250π cm³", alternativa_b="500π cm³", alternativa_c="750π cm³",
                alternativa_d="1000π cm³", alternativa_e="1500π cm³",
                resposta_correta="B"),

        # Questões de JavaScript
        Questao(texto="Qual método converte uma string para um número inteiro em JavaScript?",
                alternativa_a="parseInt()", alternativa_b="toFixed()", alternativa_c="parseFloat()",
                alternativa_d="NumberFormat()", alternativa_e="round()",
                resposta_correta="A"),

        Questao(texto="Qual é a saída do seguinte código: console.log(typeof null);",
                alternativa_a='"null"', alternativa_b='"object"', alternativa_c='"undefined"',
                alternativa_d='"boolean"', alternativa_e='"string"',
                resposta_correta="B"),

        Questao(texto="Qual dos seguintes operadores pode ser usado para verificar valores e tipos simultaneamente?",
                alternativa_a="==", alternativa_b="===", alternativa_c="!=", alternativa_d="||=",
                alternativa_e="&",
                resposta_correta="B"),

        # Questões de CSS
        Questao(texto="Qual propriedade define o espaçamento entre as letras de um texto?",
                alternativa_a="letter-spacing", alternativa_b="word-spacing", alternativa_c="line-height",
                alternativa_d="text-align", alternativa_e="font-weight",
                resposta_correta="A"),

        Questao(texto="Qual unidade de medida relativa no CSS representa a altura da letra 'M' em um elemento?",
                alternativa_a="rem", alternativa_b="vh", alternativa_c="vw", alternativa_d="em",
                alternativa_e="px",
                resposta_correta="D"),

        Questao(texto="Qual propriedade do CSS é usada para criar uma sombra em elementos?",
                alternativa_a="text-shadow", alternativa_b="box-shadow", alternativa_c="shadow",
                alternativa_d="filter-shadow", alternativa_e="opacity",
                resposta_correta="B"),
    ]

    for questao in questoes:  # Adiciona as questões ao banco, evitando duplicatas
        existente = Questao.query.filter_by(texto=questao.texto).first()
        if not existente:
            db.session.add(questao)

    db.session.commit()


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        senha = request.form.get('senha')
        aluno = Aluno.query.filter_by(cpf=cpf).first()

        # Verifica a senha criptografada
        if aluno and check_password_hash(aluno.senha_hash, senha):
            # Redireciona para a página home.html
            return redirect(url_for('home'))
        else:
            return "Erro: CPF ou senha incorretos!", 400

    return render_template('login.html')


@app.route('/home')
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
    senha = request.form.get('senha')

    if not cpf or not nome or not email or not telefone or not senha:
        return "Erro: Todos os campos devem ser preenchidos!", 400

    if Aluno.query.filter_by(cpf=cpf).first():
        return "Erro: CPF já cadastrado!", 400

    senha_hash = generate_password_hash(senha)
    novo_aluno = Aluno(cpf=cpf, nome=nome, email=email,
                       telefone=telefone, senha_hash=senha_hash)
    db.session.add(novo_aluno)
    db.session.commit()

    return redirect(url_for('login'))


@app.route('/aula')
def aula():
    return render_template('aula.html')


@app.route('/exerc')
def exerc():
    questao = Questao.query.order_by(db.func.random()).first()
    return render_template('exerc.html', questao=questao)


@app.route('/verificar_resposta', methods=['POST'])
def verificar_resposta():
    questao_id = request.form.get('questao_id')
    resposta_usuario = request.form.get('answer')

    questao = Questao.query.filter_by(id=questao_id).first()

    if questao:
        resposta_correta = questao.resposta_correta.strip().upper()
        resposta_usuario = resposta_usuario.strip().upper()
        acertou = resposta_usuario == resposta_correta

        # Salvar no histórico de respostas
        resposta = HistoricoResposta(
            questao_id=questao.id, resposta_usuario=resposta_usuario, acertou=acertou)
        db.session.add(resposta)
        db.session.commit()

        return {"correto": acertou, "mensagem": "✅ Parabéns! Resposta correta!" if acertou else "❌ Resposta incorreta. Tente novamente!"}
    else:
        return {"correto": False, "mensagem": "❌ Erro ao carregar a questão!"}


@app.route('/nova_questao')
def nova_questao():
    questao = Questao.query.order_by(db.func.random()).first()
    return {
        "id": questao.id,
        "texto": questao.texto,
        "alternativa_a": questao.alternativa_a,
        "alternativa_b": questao.alternativa_b,
        "alternativa_c": questao.alternativa_c,
        "alternativa_d": questao.alternativa_d,
        "alternativa_e": questao.alternativa_e
    }


@app.route('/jogo')
def jogo():
    return render_template('jogo.html')


@app.route('/perfil')
def perfil():
    aluno = Aluno.query.first()  # Simulação: Pegue um usuário cadastrado
    return render_template('perfil.html', aluno=aluno)


if __name__ == '__main__':
    app.run(debug=True)
