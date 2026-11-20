"""Listas de cenário do letreiro: moldura, céu, skyline, ponte, carro e helicóptero, todos sem marca nem hex solto."""
import json
import re

import pytest

from cn import prompt, termos

ELEMENTOS = {"MOLDURA": "palm", "CEU": None, "SKYLINE": None, "PONTE": "bridge|causeway", "CARRO": "car|convertible|coupe", "HELICOPTERO": "helicopter"}


@pytest.fixture(scope="module")
def listas():
    return json.loads((prompt.PASTA / "cenario-letreiro.json").read_text(encoding="utf-8"))


def test_tem_todos_os_elementos(listas):
    assert set(listas) == set(ELEMENTOS)
    for nome, padrao in ELEMENTOS.items():
        assert len(listas[nome]) >= 3, nome
        assert len(set(listas[nome])) == len(listas[nome]), f"{nome}: itens repetidos"
        if padrao:
            assert all(re.search(padrao, x) for x in listas[nome]), nome


def test_nenhuma_marca_e_nenhum_termo_bloqueado(listas):
    for nome, itens in listas.items():
        for x in itens:
            assert not termos.achar(x), f"{nome}: {x}"
            assert not re.search(r"\b[A-Z][a-z]+", x), f"{nome}: nome próprio em {x!r}"


def test_nenhum_hex_nem_texto_pedido_nas_listas(listas):
    junto = json.dumps(listas)
    assert not re.search(r"#[0-9A-Fa-f]{3,6}", junto)
    assert not re.search(r"\b(says|reads|saying|caption|slogan)\b", junto, re.IGNORECASE)


def test_helicoptero_e_carro_sem_marcacao(listas):
    assert all("no markings" in x or "no badges" in x or "unreadable" in x for x in listas["HELICOPTERO"] + listas["CARRO"])
