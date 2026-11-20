"""Peça de letreiro: 4:5 = 1080x1350, 1:1 = 1080x1080, com título, 2 painéis, faixa de chamada e rodapé; contraste e regras dos tokens."""
import json
import re
from pathlib import Path

import pytest

from cn import peca, render, termos, validar
from cn import tokens as tk


@pytest.fixture(params=list(peca.FORMATOS))
def html(request, tokens):
    return peca.pagina(tokens, request.param, peca.CONTEUDO, 1)


def test_estrutura_da_peca(html):
    assert html.count('class="cn-titulo-letreiro"') == 1
    assert html.count('class="cn-painel-letreiro"') == 2
    assert html.count('class="cn-faixa-chamada"') == 1 and html.count('class="cn-rodape"') == 1
    assert html.count('class="cn-chip-valor"') == 1, "um lima por peça, só no valor"
    assert "<svg" in html and "<img" not in html  # fundo vetorial próprio, sem imagem externa nem texto desenhado


def test_tamanhos_declarados():
    assert peca.FORMATOS == {"4:5": (1080, 1350), "1:1": (1080, 1080)}


def test_peca_passa_no_validar_e_so_usa_hex_dos_tokens(html, tokens):
    assert validar.conferir_texto("p.html", html, ".html", tokens, tk.hex_permitidos(tokens), termos.carregar()) == []
    assert {h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}", html)} <= tk.hex_permitidos(tokens)


def test_contorno_claro_so_no_painel(html, tokens):
    claro = tk.cor(tokens, "contorno-painel")
    for trecho in re.findall(r"[^{}]*\{[^{}]*" + claro + r"[^{}]*\}", html):
        seletor = trecho.split("{")[0]
        assert ":root" in seletor or "painel-letreiro" in seletor


def test_contraste_dos_pares_usados(tokens):
    assert peca.checar_pares(tokens) == []


def test_fundo_deterministico_e_varia_com_a_semente(tokens):
    a = peca.fundo_svg(tokens, "4:5", 3)
    assert a == peca.fundo_svg(tokens, "4:5", 3) and a != peca.fundo_svg(tokens, "4:5", 4)


def test_texto_e_escapado(tokens):
    c = peca.CONTEUDO | {"chamada": "<b>x</b>"}
    assert "<b>x</b>" not in peca.pagina(tokens, "1:1", c, 1)


@pytest.mark.skipif(render.chrome() is None, reason="Chrome não encontrado")
def test_cli_gera_os_dois_pngs(cli, tmp_path):
    r = cli("render", "peca", "--saida", str(tmp_path), "--semente", "2", "--json")
    assert r.returncode == 0, r.stderr
    tamanhos = {Path(t["png"]).name: tuple(t["tamanho"]) for t in json.loads(r.stdout)["pecas"]}
    assert tamanhos == {"peca-4x5.png": (1080, 1350), "peca-1x1.png": (1080, 1080)}
    assert render.tamanho_png(tmp_path / "peca-4x5.png") == (1080, 1350)


@pytest.mark.parametrize("args", [("--formato", "16:9"), ("--titulo1", "<script>"), ("--marca", "Vice City")])
def test_entrada_invalida_sai_2_ou_argparse(cli, tmp_path, args):
    r = cli("render", "peca", "--saida", str(tmp_path), *args)
    assert r.returncode == 2 and not list(tmp_path.glob("*.png"))
