
from flask import (
    Flask,
    jsonify,
    render_template,
    render_template_string,
    request
)

from produtos import cadastrar_produto, listar_produtos
from movimentacoes import movimentar_estoque, listar_movimentacoes

aplicativo = Flask(__name__)

DADOS_SISTEMA = {
    "sistema": "ARTINPACK",
    "descricao": "Sistema Web de Controle de Estoque",
    "versao": "1.0",
    "status": "em desenvolvimento"
}


@aplicativo.route("/")
def inicio():
    return render_template("index.html")


@aplicativo.route("/status")
def status():
    return jsonify({
        "mensagem": "ARTINPACK iniciado com sucesso"
    })


@aplicativo.route("/api/produtos", methods=["GET", "POST"])
def api_produtos():
    if request.method == "GET":
        return jsonify(listar_produtos())

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Envie os dados em formato JSON."
        }), 400

    try:
        produto = cadastrar_produto(
            dados.get("nome"),
            dados.get("preco"),
            dados.get("quantidade")
        )

        return jsonify({
            "mensagem": "Produto cadastrado com sucesso!",
            "produto": produto
        }), 201

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400


@aplicativo.route("/api/movimentacoes", methods=["GET", "POST"])
def api_movimentacoes():
    if request.method == "GET":
        return jsonify(listar_movimentacoes())

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Envie os dados em formato JSON."
        }), 400

    produto_id = dados.get("produto_id")
    quantidade = dados.get("quantidade")
    tipo = dados.get("tipo")

    if type(produto_id) is not int or produto_id <= 0:
        return jsonify({
            "erro": "Informe um ID de produto válido."
        }), 400

    try:
        registro = movimentar_estoque(
            produto_id,
            tipo,
            quantidade
        )

        return jsonify({
            "mensagem": "Movimentação registrada com sucesso!",
            "movimentacao": registro
        }), 201

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400


@aplicativo.route("/acessibilidade")
def acessibilidade():
    return render_template_string("""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ARTINPACK - Acessibilidade</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f3f6fc;
            color: #17233b;
            margin: 0;
            font-size: 18px;
        }

        main {
            max-width: 850px;
            margin: 40px auto;
            padding: 30px;
            background: white;
            border-radius: 12px;
        }

        h1 { color: #2349a2; }

        button {
            padding: 12px 18px;
            margin: 5px;
            font-size: 1rem;
            cursor: pointer;
            border: 2px solid currentColor;
            border-radius: 8px;
            background: #e4ebff;
            color: #17233b;
        }

        button:focus-visible {
            outline: 3px solid #e67e22;
            outline-offset: 3px;
        }

        .contraste {
            background: #000;
            color: #fff;
        }

        .contraste main {
            background: #000;
            border: 2px solid #ffeb00;
        }

        .contraste h1 { color: #ffeb00; }

        .contraste button {
            background: #ffeb00;
            color: #000;
        }
    </style>
</head>
<body>
    <main>
        <h1>ARTINPACK</h1>
        <p>Sistema Web de Controle de Estoque</p>

        <h2>Recursos de acessibilidade</h2>

        <button id="contraste" type="button"
                aria-pressed="false"
                onclick="alternarContraste()">
            Ativar alto contraste
        </button>

        <button type="button" onclick="alterarFonte(2)">
            Aumentar fonte +
        </button>

        <button type="button" onclick="alterarFonte(-2)">
            Diminuir fonte -
        </button>

        <h2>Informações do sistema</h2>
        <p><strong>Sistema:</strong> {{ dados.sistema }}</p>
        <p><strong>Descrição:</strong> {{ dados.descricao }}</p>
        <p><strong>Versão:</strong> {{ dados.versao }}</p>
        <p><strong>Status:</strong> {{ dados.status }}</p>
    </main>

    <script>
        let tamanhoFonte = 18;

        function alternarContraste() {
            const ativo = document.body.classList.toggle("contraste");
            const botao = document.getElementById("contraste");

            botao.setAttribute("aria-pressed", String(ativo));
            botao.textContent = ativo
                ? "Desativar alto contraste"
                : "Ativar alto contraste";
        }

        function alterarFonte(valor) {
            tamanhoFonte = Math.max(
                14, Math.min(30, tamanhoFonte + valor)
            );
            document.body.style.fontSize = tamanhoFonte + "px";
        }
    </script>
</body>
</html>
    """, dados=DADOS_SISTEMA)


if __name__ == "__main__":
    aplicativo.run(debug=True)
