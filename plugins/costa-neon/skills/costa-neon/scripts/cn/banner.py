"""Ilustração do banner do readme-studio (área x 770-1250, y 70-370): uma tela 16:9 em miniatura, só formas vetoriais
próprias (céu, sol listrado, palmeiras, barras e linha neon), com as cores tiradas dos tokens (ADR-0001)."""
from __future__ import annotations

from cn import tokens as tk
from cn.logo import paradas_svg

X, Y, L, A = 784, 86, 432, 243  # a tela
SOL = (1000, 250, 78)
LISTRAS = ((246, 3), (258, 5), (272, 8), (289, 12))
PALMEIRAS = ((842, 300, 846, 200), (1150, 300, 1144, 180))
FOLHAS = "q-30 -4 -46 14 M{x} {y} q-20 -22 -44 -18 M{x} {y} q10 -26 36 -26 M{x} {y} q30 -4 44 16 M{x} {y} q2 -30 -10 -40"


def ilustracao(t: dict) -> str:
    c = tk.cor_de(t)
    cx, cy, r = SOL
    defs = (f'<defs><linearGradient id="cnceu" x1="0" y1="0" x2="0" y2="1">{paradas_svg(tk.paradas(t, "ceu"))}</linearGradient>'
            f'<linearGradient id="cnsol2" x1="0" y1="0" x2="0" y2="1">{paradas_svg(tk.paradas(t, "sol"))}</linearGradient>'
            f'<linearGradient id="cnneon" x1="0" y1="0" x2="1" y2="0">{paradas_svg(tk.paradas(t, "neon"))}</linearGradient>'
            f'<clipPath id="cnsolc"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
            f'<clipPath id="cntela"><rect x="{X}" y="{Y}" width="{L}" height="{A}"/></clipPath></defs>')
    listras = "".join(f'<rect x="{cx - 100}" y="{y}" width="200" height="{h}" fill="{tk.paradas(t, "ceu")[2]}"/>' for y, h in LISTRAS)
    palmeiras = "".join(
        f'<path d="M{x0} {y0} L{x} {y}" stroke="{c("ameixa")}" stroke-width="5" fill="none"/>'
        f'<path d="M{x} {y} {FOLHAS.format(x=x, y=y)}" stroke="{c("ameixa")}" stroke-width="5" fill="none" stroke-linecap="round"/>'
        for x0, y0, x, y in PALMEIRAS)
    passaros = f'<path d="M930 150 l6 4 l6 -4 M960 138 l5 3 l5 -3 M948 166 l4 3 l4 -3" stroke="{c("malva-escuro")}" stroke-width="2" fill="none"/>'
    barras = (f'<rect x="{X}" y="{Y}" width="{L}" height="22" fill="{c("preto-barra")}"/>'
              f'<rect x="{X}" y="{Y + A - 22}" width="{L}" height="22" fill="{c("preto-barra")}"/>'
              f'<rect x="{X}" y="{Y + 21}" width="{L}" height="2" fill="url(#cnneon)"/>'
              f'<rect x="{X}" y="{Y + A - 23}" width="{L}" height="2" fill="url(#cnneon)"/>'
              f'<rect x="1104" y="91" width="60" height="12" fill="url(#cnneon)"/>'
              f'<rect x="1170" y="91" width="34" height="12" rx="2" fill="{c("chip-escuro")}"/>')
    corpo = (f'<g clip-path="url(#cntela)"><rect x="{X}" y="{Y}" width="{L}" height="{A}" fill="url(#cnceu)"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#cnsol2)"/><g clip-path="url(#cnsolc)">{listras}</g>'
             f'<path d="M784 300 Q850 286 920 298 T1060 296 T1216 292 L1216 329 L784 329 Z" fill="{c("ameixa")}"/>'
             f'{palmeiras}{passaros}{barras}</g>')
    legenda = (f'<text x="1000" y="356" text-anchor="middle" font-size="15" fill="{c("rosa-valor")}" '
               f'font-family="ui-monospace, Menlo, Consolas, monospace">tokens · validar · prompt · temas</text>')
    return defs + corpo + legenda + "\n"
