
from decimal import Decimal, InvalidOperation
from banco import conectar, inicializar_banco


def cadastrar_produto(nome, preco, quantidade):
    """Cadastra um produto no banco de dados SQLite."""

    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("O nome do produto é obrigatório.")

    try:
        preco = Decimal(str(preco))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("O preço informado é inválido.")

    if not preco.is_finite() or preco < 0:
        raise ValueError("O preço deve ser válido e não negativo.")

    if type(quantidade) is not int or quantidade < 0:
        raise ValueError(
            "A quantidade deve ser um inteiro não negativo."
        )

    inicializar_banco()

    with conectar() as conexao:
        cursor = conexao.execute(
            """
            INSERT INTO produtos (nome, preco, quantidade)
            VALUES (?, ?, ?)
            """,
            (nome.strip(), str(preco), quantidade)
        )

        produto_id = cursor.lastrowid
        conexao.commit()

    return {
        "id": produto_id,
        "nome": nome.strip(),
        "preco": str(preco),
        "quantidade": quantidade
    }


def listar_produtos():
    """Consulta todos os produtos cadastrados."""

    inicializar_banco()

    with conectar() as conexao:
        registros = conexao.execute(
            """
            SELECT id, nome, preco, quantidade
            FROM produtos
            ORDER BY id
            """
        ).fetchall()

    return [dict(produto) for produto in registros]
