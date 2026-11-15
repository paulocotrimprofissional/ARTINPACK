
from flask import Flask, jsonify

aplicativo = Flask(__name__)

@aplicativo.route("/")
def inicio():
    return jsonify({
        "sistema": "ARTINPACK",
        "descricao": "Sistema Web de Controle de Estoque",
        "versao": "1.0",
        "status": "em desenvolvimento"
    })

@aplicativo.route("/status")
def status():
    return jsonify({
        "mensagem": "ARTINPACK iniciado com sucesso"
    })

if __name__ == "__main__":
    aplicativo.run(debug=True)
