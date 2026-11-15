
from app import aplicativo


def test_pagina_inicial():
    cliente = aplicativo.test_client()
    resposta = cliente.get("/")

    assert resposta.status_code == 200

    dados = resposta.get_json()
    assert dados["sistema"] == "ARTINPACK"
    assert dados["versao"] == "1.0"


def test_status():
    cliente = aplicativo.test_client()
    resposta = cliente.get("/status")

    assert resposta.status_code == 200

    dados = resposta.get_json()
    assert dados["mensagem"] == "ARTINPACK iniciado com sucesso"
