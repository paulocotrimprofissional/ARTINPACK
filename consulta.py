
from produtos import listar_produtos


def consultar_estoque(nome=None):
    """Consulta os produtos e suas quantidades disponíveis."""
    produtos = listar_produtos()

    if nome:
        produtos = [
            produto for produto in produtos
            if nome.lower() in produto["nome"].lower()
        ]

    return produtos


def consultar_produto_por_id(produto_id):
    """Localiza um produto pelo identificador."""
    for produto in listar_produtos():
        if produto["id"] == produto_id:
            return produto

    raise ValueError("Produto não encontrado.")


def verificar_estoque_baixo(limite=10):
    """Identifica produtos com estoque abaixo do limite."""
    if type(limite) is not int or limite < 0:
        raise ValueError("O limite deve ser um inteiro não negativo.")

    return [
        produto for produto in listar_produtos()
        if produto["quantidade"] < limite
    ]
