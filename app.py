
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def inicio():
    return jsonify({
        "sistema": "ARTINPACK",
        "descricao": "Sistema Web de Controle de Estoque",
        "versao": "1.0",
        "status": "em desenvolvimento"
    })


@app.route("/status")
def status():
    return jsonify({
        "mensagem": "ARTINPACK iniciado com sucesso"
    })


if __name__ == "__main__":
    app.run(debug=True)
