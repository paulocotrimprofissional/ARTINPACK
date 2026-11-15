
from produtos import produtos

historico = []


def movimentar_estoque(produto_id, tipo, quantidade):
    if tipo not in ("entrada", "saida"):
        raise ValueError("Tipo de movimentação inválido.")

    if type(quantidade) is not int or quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")

    produto = next(
        (p for p in produtos if p["id"] == produto_id),
        None
    )

    if produto is None:
        raise ValueError("Produto não encontrado.")

    saldo_anterior = produto["quantidade"]

    if tipo == "saida":
        if quantidade > saldo_anterior:
            raise ValueError("Estoque insuficiente.")
        produto["quantidade"] -= quantidade
    else:
        produto["quantidade"] += quantidade

    registro = {
        "produto_id": produto_id,
        "tipo": tipo,
        "quantidade": quantidade,
        "saldo_anterior": saldo_anterior,
        "saldo_atual": produto["quantidade"]
    }

    historico.append(registro)
    return registro


def listar_movimentacoes():
    return historico.copy()
