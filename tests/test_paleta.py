"""Paleta deslocada (ADR-0007): 70 hex, longe do conceito e do prompt, distintos entre si."""
import itertools

from cn import tokens as tk
from conftest import DADOS


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def dist(a, b):
    return max(abs(x - y) for x, y in zip(rgb(a), rgb(b), strict=True))


def evitar():
    return [x.strip() for x in (DADOS / "evitar-hex.txt").read_text(encoding="utf-8").splitlines() if x.startswith("#") and len(x.strip()) == 7]


def test_70_hex_distintos(tokens):
    assert len(tk.hex_permitidos(tokens)) == 70


def test_longe_do_conceito_e_do_prompt(tokens):
    perto = [(h, e) for h in tk.hex_permitidos(tokens) for e in evitar() if dist(h, e) <= 3]
    assert not perto, f"hex a ±3 de um valor a evitar: {perto}"


def test_tokens_distintos_entre_si(tokens):
    hs = sorted(tk.hex_permitidos(tokens))
    assert all(dist(a, b) >= 4 for a, b in itertools.combinations(hs, 2))


def test_lista_a_evitar_tem_conceito_e_prompt():
    assert len(evitar()) > 62


def test_fontes_abertas_e_display_bowlby(tokens):
    fam = tokens["tipografia"]["familias"]
    assert fam["display"]["fonte"] == "Bowlby One"
    assert "pricedown" not in str(tokens).lower()


def test_tinta_e_escura(tokens):
    import colorsys
    luz = colorsys.rgb_to_hls(*(x / 255 for x in rgb(tk.cor(tokens, "tinta"))))[1]
    assert luz < 0.15
