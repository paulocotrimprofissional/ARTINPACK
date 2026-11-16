
from banco import conectar, inicializar_banco


def movimentar_estoque(produto_id, tipo, quantidade):
    """Registra entradas e saídas de estoque no SQLite."""

    if type(produto_id) is not int or produto_id <= 0:
        raise ValueError("ID do produto inválido.")

    if tipo not in ("entrada", "saida"):
        raise ValueError("Tipo de movimentação inválido.")

    if type(quantidade) is not int or quantidade <= 0:
        raise ValueError(
            "A quantidade deve ser maior que zero."
        )

    inicializar_banco()

    with conectar() as conexao:
        # Inicia uma transação para manter os dados consistentes.
        conexao.execute("BEGIN IMMEDIATE")

        produto = conexao.execute(
            """
            SELECT id, quantidade
            FROM produtos
            WHERE id = ?
            """,
            (produto_id,)
        ).fetchone()

        if produto is None:
            raise ValueError("Produto não encontrado.")

        saldo_anterior = produto["quantidade"]

        if tipo == "saida":
            if quantidade > saldo_anterior:
                raise ValueError("Estoque insuficiente.")

            saldo_atual = saldo_anterior - quantidade
        else:
            saldo_atual = saldo_anterior + quantidade

        # Atualiza a quantidade do produto.
        conexao.execute(
            """
            UPDATE produtos
            SET quantidade = ?
            WHERE id = ?
            """,
            (saldo_atual, produto_id)
        )

        # Registra a movimentação no histórico.
        cursor = conexao.execute(
            """
            INSERT INTO movimentacoes (
                produto_id,
                tipo,
                quantidade,
                saldo_anterior,
                saldo_atual
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                produto_id,
                tipo,
                quantidade,
                saldo_anterior,
                saldo_atual
            )
        )

        movimentacao_id = cursor.lastrowid

        conexao.commit()

    return {
        "id": movimentacao_id,
        "produto_id": produto_id,
        "tipo": tipo,
        "quantidade": quantidade,
        "saldo_anterior": saldo_anterior,
        "saldo_atual": saldo_atual
    }


def listar_movimentacoes():
    """Consulta o histórico de movimentações."""

    inicializar_banco()

    with conectar() as conexao:
        registros = conexao.execute(
            """
            SELECT
                id,
                produto_id,
                tipo,
                quantidade,
                saldo_anterior,
                saldo_atual,
                data_movimentacao
            FROM movimentacoes
            ORDER BY id DESC
            """
        ).fetchall()

    return [dict(registro) for registro in registros]
