
from decimal import Decimal, InvalidOperation

produtos = []
proximo_id = 1


def cadastrar_produto(nome, preco, quantidade):
    global proximo_id

    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("O nome do produto é obrigatório.")

    try:
        preco = Decimal(str(preco))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("O preço informado é inválido.")

    if not preco.is_finite() or preco < 0:
        raise ValueError("O preço deve ser válido e não negativo.")

    if type(quantidade) is not int or quantidade < 0:
        raise ValueError("A quantidade deve ser um inteiro não negativo.")

    produto = {
        "id": proximo_id,
        "nome": nome.strip(),
        "preco": str(preco),
        "quantidade": quantidade
    }

    produtos.append(produto)
    proximo_id += 1

    return produto


def listar_produtos():
    return produtos.copy()
