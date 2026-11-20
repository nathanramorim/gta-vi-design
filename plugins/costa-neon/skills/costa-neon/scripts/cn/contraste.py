"""Contraste WCAG 2.x por par texto/fundo (DUP-04: uma função só, reusada pelos testes e pela peça)."""
from __future__ import annotations

from cn import tokens as tk
from cn.entrada import RE_HEX, ErroDados


def luminancia(hex_: str) -> float:
    canais = [int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canais]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def razao(a: str, b: str) -> float:
    claro, escuro = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (claro + 0.05) / (escuro + 0.05)


def resolver(t: dict, ref: str) -> str:
    """Nome de cor, `degrade:indice` ou hex literal viram um hex dos tokens."""
    if RE_HEX.fullmatch(ref):
        return ref.upper()
    if ":" in ref:
        nome, i = ref.rsplit(":", 1)
        return tk.paradas(t, nome)[int(i)].upper()
    if ref in t["cores"]:
        return tk.cor(t, ref).upper()
    raise ErroDados(f"contraste: cor desconhecida {ref!r}")


def pares(t: dict) -> list[tuple[dict, float, float]]:
    """(par, razão medida, mínimo exigido) para cada par declarado em `contraste.pares`."""
    c = t["contraste"]
    return [(p, razao(resolver(t, p["texto"]), resolver(t, p["fundo"])), c["minimo-titulo" if p["papel"] == "titulo" else "minimo-texto"])
            for p in c["pares"]]
