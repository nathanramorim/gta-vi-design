"""Peça de letreiro (cartaz e post) em HTML -> PNG: título, 2 painéis, faixa de chamada e rodapé sobre um fundo SVG determinístico.

Texto sempre por HTML (nunca pela IA de imagem). Fundo próprio: degradê do céu e silhuetas vetoriais sorteadas pela semente.
"""
from __future__ import annotations

import random
from html import escape

from cn import css, fontes, letreiro
from cn import tokens as tk

L = 1080
FORMATOS = {"4:5": (1080, 1350), "1:1": (1080, 1080)}
# posições em fração da altura: título, painéis, horizonte, faixa, rodapé
LAYOUT = {"4:5": {"titulo": 60, "fonte": 150, "painel": (500, 300), "horizonte": 470, "faixa": (840, 82), "rodape": 90, "carro": 1045},
          "1:1": {"titulo": 30, "fonte": 104, "painel": (372, 300), "horizonte": 350, "faixa": (700, 70), "rodape": 80, "carro": 815}}
# Pares texto/fundo que a peça usa: todos precisam existir em `contraste.pares` dos tokens (e passam no teste).
PARES_USADOS = (("branco", "painel-letreiro"), ("rosa-valor", "painel-letreiro"), ("tinta", "lima-destaque"), ("tinta", "rosa-letreiro"),
                ("branco", "tinta"), ("rosa-letreiro", "tinta"))
CONTEUDO = {"titulo1": "Nova missão", "titulo2": "desbloqueada", "painel1-titulo": "A rota", "painel1-texto": "Três paradas na orla antes do pôr do sol.",
            "painel2-titulo": "A oferta", "painel2-texto": "Passe da temporada com acesso a todas as rotas.", "valor": "Só 49,90",
            "chamada": "Garanta o seu agora", "marca": "Palmarena Studio", "cidade": "Palmarena"}


def _palmeira(rnd: random.Random, x: float, y: float, altura: float, lado: int, cor: str) -> str:
    topo = (x + lado * altura * 0.12, y - altura)
    tronco = (f'<path d="M{x - 9:.0f} {y:.0f} Q{x + lado * 20:.0f} {y - altura * 0.5:.0f} {topo[0]:.0f} {topo[1]:.0f} '
              f'L{topo[0] + 8:.0f} {topo[1]:.0f} Q{x + lado * 34:.0f} {y - altura * 0.5:.0f} {x + 9:.0f} {y:.0f}Z" fill="{cor}"/>')
    folhas = "".join(f'<path d="M0 0 Q{rnd.randint(50, 70)} {-rnd.randint(30, 55)} {rnd.randint(120, 160)} {rnd.randint(8, 30)} '
                     f'Q{rnd.randint(60, 80)} {-rnd.randint(0, 10)} 0 0Z" fill="{cor}" transform="translate({topo[0]:.0f} {topo[1]:.0f}) rotate({a}) scale(1.3)"/>'
                     for a in range(-170, 40, 30))
    return tronco + folhas


def _skyline(rnd: random.Random, y: float, cor: str, minimo: int, maximo: int) -> str:
    x, partes = -20.0, []
    while x < L + 20:
        w, h = rnd.randint(46, 110), rnd.randint(minimo, maximo)
        partes.append(f'<rect x="{x:.0f}" y="{y - h:.0f}" width="{w}" height="{h}" fill="{cor}"/>')
        if rnd.random() < 0.4:
            partes.append(f'<rect x="{x + w * 0.2:.0f}" y="{y - h - 22:.0f}" width="{w * 0.6:.0f}" height="22" fill="{cor}"/>')
        x += w + rnd.randint(0, 8)
    return "".join(partes)


def _carro(x: float, y: float, escala: float, corpo: str, luz: str) -> str:
    return (f'<g transform="translate({x:.0f} {y:.0f}) scale({escala})"><path d="M0 110 L12 82 L92 72 L142 30 L272 30 L332 66 L392 78 L404 110Z" fill="{corpo}"/>'
            f'<circle cx="92" cy="110" r="27" fill="{corpo}"/><circle cx="312" cy="110" r="27" fill="{corpo}"/>'
            f'<path d="M142 30 L272 30 L332 66" fill="none" stroke="{luz}" stroke-width="4"/></g>')


def _helicoptero(x: float, y: float, cor: str, luz: str) -> str:
    return (f'<g transform="translate({x:.0f} {y:.0f})" stroke="{luz}" stroke-width="1.5"><ellipse cx="0" cy="0" rx="26" ry="12" fill="{cor}"/><rect x="22" y="-5" width="48" height="6" fill="{cor}"/>'
            f'<rect x="64" y="-16" width="5" height="22" fill="{cor}"/><rect x="-34" y="-17" width="68" height="4" fill="{cor}"/><rect x="-18" y="12" width="36" height="3" fill="{cor}"/></g>')


def fundo_svg(t: dict, formato: str, semente: int) -> str:
    """Fundo determinístico: céu, sol, skyline, ponte, água, palmeiras, carro e helicóptero. Só hex dos tokens."""
    w, h = FORMATOS[formato]
    lay = LAYOUT[formato]
    rnd = random.Random(semente)
    hz = lay["horizonte"]
    ceu = tk.paradas(t, "ceu-letreiro")
    c = lambda n: tk.cor(t, n)  # noqa: E731
    stops = lambda ps: "".join(f'<stop offset="{i / (len(ps) - 1):.3f}" stop-color="{p}"/>' for i, p in enumerate(ps))  # noqa: E731
    sol = tk.paradas(t, "sol")
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" class="cn-fundo" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
              f'<defs><linearGradient id="ceu" x1="0" y1="0" x2="0" y2="1">{stops(ceu)}</linearGradient>'
              f'<linearGradient id="agua" x1="0" y1="0" x2="0" y2="1">{stops(ceu[::-1])}</linearGradient>'
              f'<linearGradient id="sol" x1="0" y1="0" x2="0" y2="1">{stops(sol)}</linearGradient></defs>',
              f'<rect width="{w}" height="{hz}" fill="url(#ceu)"/>',
              f'<circle cx="{w * rnd.uniform(0.35, 0.65):.0f}" cy="{hz - 20}" r="{rnd.randint(110, 150)}" fill="url(#sol)" opacity="0.9"/>',
              _skyline(rnd, hz, c("roxo-sombra"), 40, 120),
              _skyline(rnd, hz, c("painel-letreiro"), 18, 56),
              f'<rect y="{hz}" width="{w}" height="{h - hz}" fill="url(#agua)"/>',
              f'<rect y="{hz + 10}" width="{w}" height="14" fill="{c("painel-letreiro")}"/>']
    partes += [f'<rect x="{x}" y="{hz + 24}" width="10" height="46" fill="{c("painel-letreiro")}"/>' for x in range(30, w, 130)]
    partes += [f'<rect y="{lay["carro"] + 137}" width="{w}" height="{h}" fill="{c("painel-letreiro")}"/>',
               f'<rect y="{lay["carro"] + 137}" width="{w}" height="4" fill="{c("rosa-letreiro")}"/>',
               _palmeira(rnd, 40, h * 0.99, h * rnd.uniform(0.62, 0.66), 1, c("painel-letreiro")),
               _palmeira(rnd, w - 40, h * 0.99, h * rnd.uniform(0.62, 0.66), -1, c("painel-letreiro")),
               _carro(rnd.randint(150, 320), lay["carro"], 1.0, c("painel-letreiro"), c("rosa-letreiro")),
               _helicoptero(rnd.randint(40, 56), rnd.randint(70, 110), c("painel-letreiro"), c("rosa-letreiro")), "</svg>"]
    return "".join(partes)


def _css_painel(t: dict) -> str:
    """Componente painel-letreiro: miolo escuro dentro de um contorno claro, cantos chanfrados (a exceção da Regra 8)."""
    contorno, painel = tk.cor(t, "contorno-painel"), tk.cor(t, "painel-letreiro")
    ch = lambda n: (f"polygon({n}px 0, calc(100% - {n}px) 0, 100% {n}px, 100% calc(100% - {n}px), calc(100% - {n}px) 100%, "  # noqa: E731
                    f"{n}px 100%, 0 calc(100% - {n}px), 0 {n}px)")
    return (f".cn-painel-letreiro {{ background: {contorno}; padding: 4px; clip-path: {ch(30)}; box-sizing: border-box; }}\n"
            f".cn-painel-letreiro .cn-painel-miolo {{ background: {painel}; clip-path: {ch(27)}; height: 100%; box-sizing: border-box; padding: 26px 34px; }}\n")


def pagina(t: dict, formato: str, conteudo: dict[str, str], semente: int) -> str:
    w, h = FORMATOS[formato]
    lay = LAYOUT[formato]
    c = lambda n: tk.cor(t, n)  # noqa: E731
    corpo = t["tipografia"]["familias"]["letreiro-corpo"]["pilha"]
    py, ph = lay["painel"]
    fy, fh = lay["faixa"]
    e = lambda k: escape(conteudo[k])  # noqa: E731
    sombra = t["sombras"]["titulo-letreiro"]["valor"]
    estilo = (f"html, body {{ margin: 0; width: {w}px; height: {h}px; overflow: hidden; font-family: {corpo}; }}\n"
              f".cn-fundo {{ position: absolute; left: 0; top: 0; }}\n"
              f".cn-titulo-letreiro {{ position: absolute; left: 0; right: 0; top: {lay['titulo']}px; text-align: center; font-size: {lay['fonte']}px; }}\n"
              f".cn-paineis {{ position: absolute; left: 56px; right: 56px; top: {py}px; height: {ph}px; display: flex; gap: 34px; }}\n"
              f".cn-paineis .cn-painel-letreiro {{ flex: 1; }}\n"
              f".cn-painel-miolo h2 {{ margin: 0 0 12px; font-size: 40px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: {c('rosa-valor')}; }}\n"
              f".cn-painel-miolo p {{ margin: 0; font-size: 36px; font-weight: 600; line-height: 1.2; color: {c('branco')}; }}\n"
              f".cn-chip-valor {{ display: inline-block; margin-top: 16px; padding: 4px 22px; border-radius: 999px; background: {c('lima-destaque')}; color: {c('tinta')}; font-size: 46px; font-weight: 700; }}\n"
              f".cn-faixa-chamada {{ position: absolute; left: -20px; right: -20px; top: {fy}px; height: {fh}px; background: {c('rosa-letreiro')}; color: {c('tinta')};"
              f" transform: rotate(-1.5deg); display: flex; align-items: center; justify-content: center; font-size: 52px; font-weight: 700; text-transform: uppercase;"
              f" letter-spacing: 0.06em; box-shadow: {sombra}; }}\n"
              f".cn-rodape {{ position: absolute; left: 0; right: 0; bottom: 0; height: {lay['rodape']}px; background: {c('painel-letreiro')}; color: {c('branco')};"
              f" display: flex; align-items: center; justify-content: space-between; padding: 0 56px; font-size: 32px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }}\n")
    faces = fontes.face_css(t, "gigante") + "\n" + fontes.face_css(t, "letreiro-corpo")
    return (f'<!doctype html><html lang="pt-BR"><meta charset="utf-8"><style>\n{faces}\n{css.gerar(t)}\n{estilo}{letreiro.estilo_titulo(t)}{_css_painel(t)}</style>'
            f'<body>{fundo_svg(t, formato, semente)}{letreiro.titulo_html(conteudo["titulo1"], conteudo["titulo2"])}'
            f'<div class="cn-paineis"><div class="cn-painel-letreiro"><div class="cn-painel-miolo"><h2>{e("painel1-titulo")}</h2><p>{e("painel1-texto")}</p></div></div>'
            f'<div class="cn-painel-letreiro"><div class="cn-painel-miolo"><h2>{e("painel2-titulo")}</h2><p>{e("painel2-texto")}</p>'
            f'<span class="cn-chip-valor">{e("valor")}</span></div></div></div>'
            f'<div class="cn-faixa-chamada">{e("chamada")}</div>'
            f'<div class="cn-rodape"><span>{e("marca")}</span><span>{e("cidade")}</span></div></body></html>\n')


def checar_pares(t: dict) -> list[str]:
    """Pares usados pela peça que não estão (ou não passam) em `contraste.pares` dos tokens."""
    from cn import contraste
    declarados = {(p["texto"], p["fundo"]): (r, m) for p, r, m in contraste.pares(t)}
    return [f"{a}/{b}" for a, b in PARES_USADOS if (a, b) not in declarados or declarados[(a, b)][0] < declarados[(a, b)][1]]


