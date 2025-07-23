# ---------------------------- Bibliotecas
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_cors import CORS
from flasgger import Swagger
from dotenv import load_dotenv

import os as osBib

from utils import logger
from utils.GeraEmail import send_email


# ---------------------------- Inicializacao
load_dotenv()


app = Flask(__name__)
app.secret_key = osBib.environ.get("FLASK_SECRET_KEY")
CORS(app)
swagger = Swagger(
    app,
    config={
        "title": "API BP",
        "uiversion": 3,
        "version": "1.0.0",
        "description": "Api Boilerplater",
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/apispec_1.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        # "static_folder": "static",  # must be set by user
        "swagger_ui": True,
        "specs_route": "/docs/",
    },
)


# ---------------------------- Rotas
@app.route('/', methods=['GET', 'POST'])
def home():
    # Verifica se o formulário foi enviado (método POST)
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        area = request.form.get('area_de_interesse')

        # --- LÓGICA DE VALIDAÇÃO E ENVIO DE MENSAGENS ---

        # Cenário de ERRO: Verifica se algum campo obrigatório está vazio
        if not nome or not email or not area or not telefone:
            flash('Por favor, preencha todos os campos obrigatórios.', 'error')

        # Cenário de SUCESSO: Se todos os campos estão preenchidos
        else:
            send_email(nome, email, area)
            
            # Envia uma mensagem de sucesso (qualquer categoria que não seja 'error')
            flash('Cadastro realizado com sucesso!\nEm breve você receberá o retorno por e-mail.', 'success')
            # Redireciona de volta para a página do formulário para exibir o sucesso

            
        return redirect(url_for('home'))

    # Se for um acesso normal (método GET), apenas exibe a página
    return render_template('home.html')

@app.route('/teste', methods=['GET', 'POST'])
def home_teste():
    # Verifica se o formulário foi enviado (método POST)
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        #area = request.form.get('area_de_interesse')

        # --- LÓGICA DE VALIDAÇÃO E ENVIO DE MENSAGENS ---

        # Cenário de ERRO: Verifica se algum campo obrigatório está vazio
        if not nome or not email or not telefone:
            flash('Por favor, preencha todos os campos obrigatórios.', 'error')

        # Cenário de SUCESSO: Se todos os campos estão preenchidos
        else:
            areas = [
                "Arquitetura e Urbanismo",
                "Automação Industrial",
                "Biologia",
                "Biologia formação de professor",
                "Biomedicina",
                "Ciências Aeronáuticas",
                "Comércio Exterior",
                "Ciência Da Computação",
                "Engenharia de Computação",
                "Fotografia",
                "Gastronomia",
                "Geografia formação de professor",
                "Gestão ambiental",
                "Gestão comercial",
                "Gestão da tecnologia da informação",
                "Gestão de negócios",
                "Gestão de pessoas",
                "Agronegócio",
                "Relações públicas",
                "Segurança da informação",
                "Segurança pública",
                "Serviço social",
                "Sistemas de informação",
                "Teologia",
                "Terapia Ocupacional",
                "Zootecnia"
            ]
            for area in areas:
                send_email(nome, email, area)

            
            # Envia uma mensagem de sucesso (qualquer categoria que não seja 'error')
            flash('Cadastro realizado com sucesso!\nEm breve você receberá o retorno por e-mail.', 'success')
            # Redireciona de volta para a página do formulário para exibir o sucesso

            
        return redirect(url_for('home_teste'))

    # Se for um acesso normal (método GET), apenas exibe a página
    return render_template('home_teste.html')

@app.route('/termo', methods=['GET'])
def termo():
    """
    Rota para exibir o termo de consentimento.
    ---
    responses:
        200:
            description: Exibe o termo de consentimento.
    """
    return render_template('termo.html')

# -------------------------------------- Main
if __name__ == "__main__":
    
    from utils.StringToBool import string_to_bool

    logger.debug("Iniciando app...")
    # print(app.url_map)
    
    app.run(
        debug=string_to_bool(osBib.environ.get("DEBUG", "False")),
        host="0.0.0.0",
        port=int(osBib.environ.get("PORT", 8080)),
    )
