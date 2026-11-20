"""tema: um arquivo no formato que cada ferramenta já lê (ADR-0005), mais a prévia para conferência visual."""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

from cn import banner, logo
from cn import tokens as tk

CONSUMIDORES = ("carrossel", "video", "readme", "forge-sdd")
MISSOES = (("Concepção", "Missão 1: o plano", "energia"), ("Planejamento", "Missão 2: a rota", "magenta"),
           ("Construção", "Missão 3: a obra", "apoio-ciano"), ("Governança", "Missão 4: o vigia", "vida"),
           ("Operação", "Missão 5: missão cumprida", "mapa-parque"))
# O carrossel-studio pede o título em 400, 500 e 600; Bowlby One só tem 400, então o título do arquivo de marca usa a
# família de HUD (Oswald). Os nomes vêm do tokens.json.
PAPEIS_FONTE_MARCA = {"title": "hud", "body": "texto", "mono": "mono"}


def _j(dado: dict) -> str:
    return json.dumps(dado, ensure_ascii=False, indent=2) + "\n"


def letreiro(t: dict) -> dict:
    """Cores, degradê e fontes do letreiro (02): chaves extras que os consumidores ignoram até quererem a peça de letreiro."""
    fam = t["tipografia"]["familias"]
    estilo = t["tipografia"]["estilos"]["titulo-letreiro"]
    cores = {"lima": "lima-destaque", "painel": "painel-letreiro", "contorno-painel": "contorno-painel", "rosa": "rosa-letreiro", "sombra": "roxo-sombra"}
    return {"cores": {k: tk.cor(t, n) for k, n in cores.items()}, "ceu": tk.paradas(t, "ceu-letreiro"), "contorno-titulo": tk.cor(t, estilo["contorno"]),
            "fontes": {"titulo": fam[estilo["familia"]]["fonte"], "corpo": fam["letreiro-corpo"]["fonte"]}}


def marca(t: dict, logo_em: str = "marca/logo.svg") -> dict:
    """Arquivo de marca do carrossel-studio e do gerador-videos (mesmos papéis). `logo_em` é relativo a quem lê."""
    fam = t["tipografia"]["familias"]
    c = lambda n: tk.cor(t, n)  # noqa: E731
    return {"cores": {"bg": c("preto-barra"), "surface": c("chip-escuro"), "text": c("branco"), "muted": c("rosa-valor"),
                      "accent": tk.paradas(t, "acento")[1], "accent2": c("laranja-selecao"), "success": c("mapa-parque"),
                      "danger": c("atributo-perda")},
            "fontes": {papel: fam[f]["fonte"] for papel, f in PAPEIS_FONTE_MARCA.items()}, "logo": logo_em,
            "letreiro": letreiro(t)}


def identidade(t: dict) -> dict:
    c = lambda n: tk.cor(t, n)  # noqa: E731
    fam = t["tipografia"]["familias"]
    return {"fundo": c("preto-barra"), "brilho": c("ameixa"), "texto": c("branco"), "suave": c("rosa-valor"),
            "acento": tk.paradas(t, "acento"), "painel": c("chip-escuro"), "borda": c("malva-escuro"),
            "terminal_fundo": c("preto-barra"), "terminal_borda": c("malva-escuro"), "ok": c("mapa-parque"),
            "fonte": fam["texto"]["pilha"], "fonte_mono": fam["mono"]["pilha"], "logo": "logo.svg.frag"}


def forge_sdd(t: dict) -> dict:
    c = lambda n: tk.cor(t, n)  # noqa: E731
    fam = t["tipografia"]["familias"]
    return {"tema": t["sistema"], "edicao": "Edição Missões", "versao_tokens": t["versao"],
            "missoes": [{"n": i, "estacao": e, "titulo": ti, "cor": c(cor)} for i, (e, ti, cor) in enumerate(MISSOES, 1)],
            "cores": {"fundo": c("preto-barra"), "texto": c("branco"), "suave": c("rosa-valor"), "contorno": c("tinta"),
                      "painel": c("chip-escuro"), "destaque": c("laranja-selecao")},
            "letreiro": letreiro(t),
            "degrades": {k: tk.degrade_css(t, k) for k in ("sunset", "acento", "neon", "sol", "ceu", "ceu-letreiro")},
            "fontes": {k: fam[k]["fonte"] for k in ("display", "texto", "script", "gigante", "hud", "mono", "letreiro-corpo")},
            "regras": ["Homenagem ao clima, sem logo, letreiro, personagem, mapa, interface ou fonte de obra existente.",
                       "Letreiro em Bowlby One branca com contorno na tinta, sobre o sol listrado.",
                       "Uma peça, um destaque: só um item com o degradê de acento por vez."],
            "logo": "logo.svg"}


def arquivos(consumidor: str, t: dict) -> dict[str, str]:
    """Nome relativo -> conteúdo. Nada é gravado aqui."""
    if consumidor == "carrossel":
        return {"marca.json": _j(marca(t)), "marca/logo.svg": logo.svg(t)}
    if consumidor == "video":
        # O gerador-videos lê conteudo/.video-marca.json e resolve o logo a partir da raiz do projeto: --saida = raiz.
        return {"conteudo/.video-marca.json": _j(marca(t, "conteudo/marca/logo.svg")), "conteudo/marca/logo.svg": logo.svg(t)}
    if consumidor == "readme":
        return {"identidade.json": _j(identidade(t)), "logo.svg.frag": logo.fragmento(t) + "\n",
                "ilustracao.svg.frag": banner.ilustracao(t)}
    if consumidor == "forge-sdd":
        return {"forge-sdd-missoes.json": _j(forge_sdd(t)), "logo.svg": logo.svg(t)}
    raise ValueError(consumidor)


def previa(consumidor: str, t: dict) -> str:
    """SVG com o emblema, o nome do tema e as amostras de cor, para olhar antes de entregar."""
    fundo, texto, suave, tinta, borda = (tk.cor(t, n) for n in ("preto-barra", "branco", "rosa-valor", "tinta", "malva-escuro"))
    fam = t["tipografia"]["familias"]
    if consumidor == "forge-sdd":
        amostras = [(m["titulo"], m["cor"]) for m in forge_sdd(t)["missoes"]]
    elif consumidor == "readme":
        d = identidade(t)
        amostras = [(k, d[k]) for k in ("fundo", "brilho", "texto", "suave", "painel", "borda", "ok")] + [(f"acento {i + 1}", a) for i, a in enumerate(d["acento"])]
    else:
        amostras = list(marca(t)["cores"].items())
    larg, alt = 1200, 260 + 92 * ((len(amostras) + 3) // 4)
    neon = tk.paradas(t, "neon")
    stops = logo.paradas_svg(neon)
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{larg}" height="{alt}" viewBox="0 0 {larg} {alt}">',
              f'<defs><linearGradient id="pvneon" x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient></defs>',
              f'<rect width="{larg}" height="{alt}" fill="{fundo}"/>',
              f'<rect y="150" width="{larg}" height="3" fill="url(#pvneon)"/>',
              f'<svg x="48" y="28" width="96" height="96" viewBox="0 0 32 32">{logo.fragmento(t, "pvlogo")}</svg>',
              f'<text x="168" y="86" font-family="{escape(fam["display"]["pilha"])}" font-size="46" fill="{texto}" stroke="{tinta}" stroke-width="2" paint-order="stroke">{escape(t["sistema"])}</text>',
              f'<text x="170" y="120" font-family="{escape(fam["texto"]["pilha"])}" font-size="22" fill="{suave}">tema {escape(consumidor)}</text>']
    for i, (nome, cor) in enumerate(amostras):
        x, y = 48 + (i % 4) * 282, 190 + (i // 4) * 92
        partes += [f'<rect x="{x}" y="{y}" width="64" height="64" fill="{cor}" stroke="{borda}" stroke-width="2"/>',
                   f'<text x="{x + 80}" y="{y + 28}" font-family="{escape(fam["texto"]["pilha"])}" font-size="18" fill="{texto}">{escape(nome)}</text>',
                   f'<text x="{x + 80}" y="{y + 52}" font-family="{escape(fam["mono"]["pilha"])}" font-size="16" fill="{suave}">{cor}</text>']
    return "".join(partes) + "</svg>\n"


def gerar(consumidor: str, t: dict, saida: Path, com_previa: bool, gravar: bool) -> list[Path]:
    """Grava só dentro de `saida` (SEG-02), sobrescrevendo os arquivos do tema; com gravar=False só lista (ARQ-05)."""
    conteudo = arquivos(consumidor, t)
    if com_previa:
        conteudo[f"previa-{consumidor}.svg"] = previa(consumidor, t)
    destinos = []
    for nome, texto in conteudo.items():
        destino = saida / nome
        destinos.append(destino)
        if gravar:
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(texto, encoding="utf-8", newline="\n")
    return destinos
