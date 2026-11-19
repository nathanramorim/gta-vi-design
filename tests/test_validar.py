"""validar: artefatos oficiais passam; cada fixture ruim sai 2 com a regra certa."""
import json

import pytest

from cn import termos, validar
from cn import tokens as tk
from conftest import DADOS, RAIZ

BOM = "#FE7688"  # acento[1] dos tokens


def problemas(nome, texto, tokens, sufixo=None):
    from pathlib import Path
    return validar.conferir_texto(nome, texto, sufixo or Path(nome).suffix, tokens, tk.hex_permitidos(tokens), termos.carregar())


def regras(ps):
    return {p.regra for p in ps}


def test_repositorio_passa(cli):
    r = cli("validar", "--json")
    assert r.returncode == 0, r.stdout
    assert json.loads(r.stdout)["ok"] is True


@pytest.mark.parametrize("nome,texto,regra", [
    ("a.css", ".x { color: #123456; }", "hex"),
    ("a.css", ".x { color: #fff; }", "hex"),
    ("a.css", ".x { color: #000000; }", "preto"),
    ("a.css", ".x { color: black; }", "preto"),
    ("a.css", ".x { box-shadow: 4px 4px 0 rgba(10,10,10,0.5); }", "sombra"),
    ("a.css", ".x { box-shadow: 0 8px 16px #FFBC49; }", "sombra"),
    ("a.css", ".x { text-shadow: 2px 2px 0; }", "sombra"),
    ("a.css", ".x { -webkit-text-stroke: 3px #1C171A; }", "contorno"),
    ("a.svg", '<path stroke="#33292F" d="M0 0"/>', "contorno"),
    ("telas/01.html", "<div class='cn-barra-topo'></div>", "tela"),
    ("a.md", "Fonte display: Pricedown Black", "termo"),
    ("a.txt", "a skyline like Vice City at dusk", "termo"),
])
def test_fixture_ruim(nome, texto, regra, tokens):
    assert regra in regras(problemas(nome, texto, tokens))


@pytest.mark.parametrize("nome,texto", [
    ("a.css", f".x {{ color: {BOM}; }}"),
    ("a.css", ".x { text-shadow: 0 0 8px #FF8484; }"),
    ("a.css", ".x { box-shadow: 0 40px 80px rgba(44,12,48,0.45); }"),
    ("a.css", ".x { text-shadow: 2px 2px 0 #49283E; }"),
    ("a.css", ".x { -webkit-text-stroke: 3px #241E27; }"),
    ("a.svg", '<path stroke="#FCFBFB" d="M0 0"/>'),
    ("a.md", "Veja o PR #111 e a seção #faq."),
    ("telas/01.html", "<i class='cn-barra-topo cn-linha-neon'></i><i class='cn-barra-base cn-linha-neon'></i>"),
])
def test_fixture_boa(nome, texto, tokens):
    assert not problemas(nome, texto, tokens)


def test_cli_sai_2_com_problema(tmp_path, cli):
    (tmp_path / "ruim.css").write_text(".x { color: #123456; }", encoding="utf-8")
    r = cli("validar", str(tmp_path), "--json")
    assert r.returncode == 2
    assert json.loads(r.stdout)["problemas"][0]["regra"] == "hex"


def test_cli_caminho_inexistente(cli, tmp_path):
    assert cli("validar", str(tmp_path / "nada")).returncode == 2


def test_hashes_batem_com_a_lista_legivel():
    claros = [x.strip() for x in (DADOS / "termos-bloqueados-claro.txt").read_text(encoding="utf-8").splitlines() if x.strip() and not x.startswith("#")]
    assert {termos.resumo(c) for c in claros} == termos.carregar()


def test_ignora_prompt_literal_e_sdd():
    alvos = validar.arquivos([RAIZ / "docs", RAIZ / "sdd"])
    assert not any(p.name == "prompt-diretor-de-arte.md" or "sdd" in p.parts for p in alvos)
