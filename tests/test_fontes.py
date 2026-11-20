"""Fontes de letreiro: licença aberta (OFL ou Apache), nome fora da lista bloqueada, estilo e render conferidos."""
import json

import pytest

from cn import css, fontes, letreiro, render, termos, validar
from cn import tokens as tk

ABERTAS = ("OFL-1.1", "Apache-2.0")


def test_toda_familia_tem_licenca_aberta_e_nome_liberado(tokens):
    for nome, f in tokens["tipografia"]["familias"].items():
        assert f["licenca"] in ABERTAS, nome
        assert not termos.achar(f["fonte"]), f"{nome}: fonte bloqueada"
        assert "pricedown" not in json.dumps(f).lower()


def test_fonte_do_letreiro_e_corpo(tokens):
    fam = tokens["tipografia"]["familias"]
    est = tokens["tipografia"]["estilos"]["titulo-letreiro"]
    assert fam[est["familia"]]["fonte"] == "Anton"
    assert fam["letreiro-corpo"]["fonte"] == "Barlow Condensed" and {600, 700} <= set(fam["letreiro-corpo"]["pesos"])
    assert fam["display"]["fonte"] == "Bowlby One"  # o display padrão da Regra 4 não muda


def test_estilo_titulo_segue_a_regra_8(tokens):
    est = tokens["tipografia"]["estilos"]["titulo-letreiro"]
    assert tk.cor(tokens, est["contorno"]) == tk.cor(tokens, "tinta")
    assert est["contorno-px"] == [3, 4]
    assert est["linha-1"] == "branco" and est["linha-2"] == "rosa-letreiro"
    assert validar.roxa_ou_azul(tuple(int(tk.cor(tokens, "roxo-sombra")[i:i + 2], 16) for i in (1, 3, 5)))


def test_css_tem_o_estilo(tokens):
    texto = css.gerar(tokens)
    assert "--cn-titulo-letreiro-contorno: 4px;" in texto and "--cn-sombra-titulo-letreiro: 4px 4px 0 #4A2C9A;" in texto
    assert "--cn-fonte-letreiro-corpo:" in texto


def test_estilo_gerado_passa_no_validar(tokens):
    html = letreiro.estilo_titulo(tokens) + letreiro.titulo_html("a", "b")
    assert validar.conferir_texto("t.html", html, ".html", tokens, tk.hex_permitidos(tokens), termos.carregar()) == []


def test_licenca_na_api_do_fontsource(tokens):
    try:
        for f in tokens["tipografia"]["familias"].values():
            meta = fontes.metadados(f["fontsource"])
            assert meta["license"] in ABERTAS and meta["license"] == f["licenca"], f["fonte"]
    except Exception as e:  # sem rede não há o que conferir
        if isinstance(e, AssertionError):
            raise
        pytest.skip(f"fontsource fora do ar: {e}")


def test_endereco_fora_do_fontsource_e_barrado():
    from cn.entrada import ErroDados
    with pytest.raises(ErroDados):
        fontes._ler("https://example.com/x.woff2")


@pytest.mark.skipif(render.chrome() is None, reason="Chrome não encontrado")
def test_amostra_renderiza_em_png(tokens, tmp_path):
    html = tmp_path / "a.html"
    html.write_text(letreiro.amostra(tokens, "Nova missão", "desbloqueada"), encoding="utf-8")
    assert render.png(html, tmp_path / "a.png", 1080, 640) == (1080, 640)
