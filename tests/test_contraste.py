"""Contraste do letreiro: todo par texto/fundo declarado nos tokens passa (WCAG: 4,5:1 texto, 3:1 título)."""
import pytest

from cn import contraste
from cn import tokens as tk
from cn.entrada import ErroDados


def test_razao_conhecida():
    assert contraste.razao("#000000", "#FFFFFF") == pytest.approx(21.0)
    assert contraste.razao("#FFFFFF", "#FFFFFF") == pytest.approx(1.0)
    assert contraste.razao("#777777", "#FFFFFF") == pytest.approx(4.48, abs=0.02)


def test_resolver_degrade_e_erro(tokens):
    assert contraste.resolver(tokens, "ceu-letreiro:0") == tk.paradas(tokens, "ceu-letreiro")[0].upper()
    with pytest.raises(ErroDados):
        contraste.resolver(tokens, "inventada")


def test_todo_par_do_letreiro_passa(tokens):
    ps = contraste.pares(tokens)
    assert len(ps) >= 8
    reprovados = [(p["texto"], p["fundo"], round(r, 2), minimo) for p, r, minimo in ps if r < minimo]
    assert not reprovados, reprovados


def test_minimos_sao_os_da_wcag(tokens):
    assert tokens["contraste"]["minimo-texto"] >= 4.5
    assert tokens["contraste"]["minimo-titulo"] >= 3


def test_lima_e_um_so_e_vive_no_painel(tokens):
    lima = tk.cor(tokens, "lima-destaque")
    assert contraste.razao(lima, tk.cor(tokens, "painel-letreiro")) >= 4.5
