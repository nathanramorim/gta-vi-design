"""Título de letreiro (estilo `titulo-letreiro` dos tokens) e a página de amostra, para olhar o PNG (Regra 11)."""
from __future__ import annotations

from html import escape

from cn import css, fontes
from cn import tokens as tk


def estilo_titulo(t: dict) -> str:
    """CSS da classe .cn-titulo-letreiro, tudo lido do tokens.json. Literais, para o `validar` conseguir conferir."""
    e = t["tipografia"]["estilos"]["titulo-letreiro"]
    fam = t["tipografia"]["familias"][e["familia"]]
    px = e["contorno-px"][-1]
    sombra = t["sombras"][e["sombra"]]["valor"]
    return (f".cn-titulo-letreiro {{ font-family: {fam['pilha']}; text-transform: uppercase; letter-spacing: {e['espacamento']};"
            f" line-height: {e['entrelinha']}; transform: rotate({e['inclinacao-graus']}deg); -webkit-text-stroke: {2 * px}px {tk.cor(t, e['contorno'])};"
            f" paint-order: stroke fill; text-shadow: {sombra}; margin: 0; background: {tk.cor(t, e['fundo'])}; padding: 0.1em 0; }}\n"
            f".cn-titulo-letreiro .l1 {{ display: block; color: {tk.cor(t, e['linha-1'])}; }}\n"
            f".cn-titulo-letreiro .l2 {{ display: block; color: {tk.cor(t, e['linha-2'])}; }}\n")


def titulo_html(linha1: str, linha2: str) -> str:
    return f'<h1 class="cn-titulo-letreiro"><span class="l1">{escape(linha1)}</span><span class="l2">{escape(linha2)}</span></h1>'


def amostra(t: dict, linha1: str, linha2: str, largura: int = 1080, altura: int = 640) -> str:
    """Página de amostra: o título sobre o degradê do céu, com a tabela de cores do estilo."""
    face = fontes.face_css(t, t["tipografia"]["estilos"]["titulo-letreiro"]["familia"])
    return (f"<!doctype html><html lang=\"pt-BR\"><meta charset=\"utf-8\"><style>\n{face}\n{css.gerar(t)}\n"
            f"html, body {{ margin: 0; width: {largura}px; height: {altura}px; }}\n"
            f"body {{ background: var(--cn-degrade-ceu-letreiro); display: flex; align-items: flex-start; justify-content: center; padding-top: 50px; box-sizing: border-box; }}\n"
            f".cn-titulo-letreiro {{ font-size: 128px; padding: 0 40px; }}\n{estilo_titulo(t)}</style><body>{titulo_html(linha1, linha2)}</body></html>\n")
