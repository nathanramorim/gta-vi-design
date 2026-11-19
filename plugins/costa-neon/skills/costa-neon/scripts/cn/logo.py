"""Emblema próprio do Costa Neon: sol retrô com listras que engrossam (nenhum logo existente)."""
from __future__ import annotations

from cn import tokens as tk

# Faixas visíveis do sol (y, altura) num quadro 32x32; os vãos entre elas são as listras.
FAIXAS = ((3, 14), (17.6, 2.2), (21.4, 1.9), (25.1, 1.5))


def _defs(t: dict, prefixo: str) -> str:
    sol = tk.paradas(t, "sol")
    neon = tk.paradas(t, "neon")
    passos = lambda cs: "".join(f'<stop offset="{i / (len(cs) - 1):.2f}" stop-color="{c}"/>' for i, c in enumerate(cs))  # noqa: E731
    faixas = "".join(f'<rect x="0" y="{y}" width="32" height="{h}"/>' for y, h in FAIXAS)
    return (f'<defs><linearGradient id="{prefixo}sol" x1="0" y1="0" x2="0" y2="1">{passos(sol)}</linearGradient>'
            f'<linearGradient id="{prefixo}neon" x1="0" y1="0" x2="1" y2="0">{passos(neon)}</linearGradient>'
            f'<clipPath id="{prefixo}faixas">{faixas}</clipPath></defs>')


def fragmento(t: dict, prefixo: str = "cnlogo") -> str:
    """Só as formas, em viewBox 32x32 (para o banner do readme-studio)."""
    return (_defs(t, prefixo) + f'<circle cx="16" cy="15" r="12" fill="url(#{prefixo}sol)" clip-path="url(#{prefixo}faixas)"/>'
            f'<rect x="4" y="28.6" width="24" height="1.8" rx="0.9" fill="url(#{prefixo}neon)"/>')


def svg(t: dict, tamanho: int = 256) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="{tamanho}" height="{tamanho}" '
            f'role="img" aria-label="{t["sistema"]}">{fragmento(t)}</svg>\n')
