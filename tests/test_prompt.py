"""prompt: 6 modos, semente determinística, borda e nada fora dos tokens."""
import json
import re

import pytest

from cn import prompt
from cn import tokens as tk


def gerar(cli, *args):
    r = cli("prompt", *args, "--json")
    return r, (json.loads(r.stdout) if r.stdout.strip() else None)


@pytest.mark.parametrize("args", [
    ("--modo", "2", "--foto-autorizada", "--semente", "3"),
    ("--modo", "3", "--semente", "3"),
    ("--modo", "4", "--semente", "3"),
    ("--modo", "6", "--tema", "capa", "--descricao", "a pink motel sign at dusk", "--semente", "3"),
])
def test_comeca_pelo_bloco_de_estilo(cli, args):
    r, d = gerar(cli, *args)
    assert r.returncode == 0, r.stderr
    assert d["texto"].startswith(prompt.estilo())
    assert "No text." in d["texto"]
    assert "{" not in d["texto"]


def test_mesma_semente_mesmo_texto(cli):
    a = gerar(cli, "--modo", "3", "--semente", "42")[1]["texto"]
    b = gerar(cli, "--modo", "3", "--semente", "42")[1]["texto"]
    assert a == b


def test_sementes_variam_pessoa(cli):
    pessoas = {gerar(cli, "--modo", "3", "--semente", str(s))[1]["valores"]["PESSOA"] for s in range(12)}
    assert len(pessoas) >= 4


def test_modo_2_sem_autorizacao_sai_2(cli):
    r, d = gerar(cli, "--modo", "2")
    assert r.returncode == 2 and "autoriz" in d["erro"]


@pytest.mark.parametrize("args", [
    ("--modo", "4", "--cidade", "Vice City"),
    ("--modo", "4", "--cidade", "<script>"),
    ("--modo", "6", "--tema", "capa", "--descricao", "a poster for GTA VI"),
    ("--modo", "6", "--tema", "inexistente", "--descricao", "x"),
    ("--modo", "6", "--tema", "capa"),
    ("--modo", "5", "--tipo", "poema"),
    ("--modo", "3", "--formato", "4:3"),
])
def test_entrada_invalida_sai_2(cli, args):
    r, d = gerar(cli, *args)
    assert r.returncode == 2
    assert d["ok"] is False


def test_modo_1_e_5_em_portugues(cli):
    m1 = gerar(cli, "--modo", "1", "--marca", "Acme")[1]["texto"]
    assert "tokens build" in m1 and "Acme" in m1
    m5 = gerar(cli, "--modo", "5", "--tipo", "sinopse", "--cidade", "Palmarena")[1]["texto"]
    assert "Palmarena" in m5 and "30 a 45 palavras" in m5


def test_modo_6_formato_e_montagem_do_tema(cli):
    d = gerar(cli, "--modo", "6", "--tema", "story", "--descricao", "a surf instructor on the shore", "--marca", "Acme")[1]
    assert d["texto"].endswith("Format 9:16.")
    assert d["montagem"].startswith("Story 9:16")


def test_so_hex_dos_tokens(cli, tokens):
    permitidos = tk.hex_permitidos(tokens)
    for modo in ("2", "3", "4"):
        extra = ("--foto-autorizada",) if modo == "2" else ()
        texto = gerar(cli, "--modo", modo, "--semente", "1", *extra)[1]["texto"]
        assert {h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}", texto)} <= permitidos
