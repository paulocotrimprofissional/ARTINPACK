
import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parent / "artinpack.db"


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def inicializar_banco():
    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco TEXT NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 0
                    CHECK (quantidade >= 0)
            )
        """)

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL
                    CHECK (tipo IN ('entrada', 'saida')),
                quantidade INTEGER NOT NULL
                    CHECK (quantidade > 0),
                saldo_anterior INTEGER NOT NULL,
                saldo_atual INTEGER NOT NULL,
                data_movimentacao TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (produto_id)
                    REFERENCES produtos(id)
            )
        """)

        conexao.commit()


if __name__ == "__main__":
    inicializar_banco()
    print("Banco de dados ARTINPACK criado com sucesso!")
