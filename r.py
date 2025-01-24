from flask import Flask
from flask_ngrok import run_with_ngrok

# Criação da aplicação Flask
app = Flask(__name__)

# Inicializa o ngrok para expor a aplicação
run_with_ngrok(app)

@app.route("/")
def home():
    return "Olá, esta é minha aplicação Flask rodando com ngrok!"

if __name__ == "__main__":
    app.run()
