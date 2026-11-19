"""tokens build: gera o costa-neon.css (uma variável por token)."""
from __future__ import annotations

from pathlib import Path

from cn import tokens as tk

ARQUIVO = tk.ARQUIVO.with_name("costa-neon.css")


def gerar(t: dict) -> str:
    v: list[tuple[str, str]] = []
    v += [(f"cor-{k}", c["valor"]) for k, c in t["cores"].items()]
    v += [(f"degrade-{k}", tk.degrade_css(t, k)) for k in t["degrades"]]
    tip = t["tipografia"]
    v += [(f"fonte-{k}", f["pilha"]) for k, f in tip["familias"].items()]
    v += [(f"tamanho-{k}", f"{px}px") for k, px in tip["escala-px"].items()]
    v += [(f"peso-{k}", str(p)) for k, p in tip["pesos"].items()]
    v += [("titulo-espacamento", tip["titulo-espacamento"]), ("corpo-entrelinha", str(tip["corpo-entrelinha"])),
          ("display-contorno", f"{tip['display-contorno-px'][0]}px")]
    e = t["espacamento"]
    v += [("espaco-base", f"{e['base-px']}px"), ("margem-lateral", e["margem-lateral"]),
          ("barra-altura", e["barra-altura"]), ("barra-altura-post", e["barra-altura-post"])]
    v += [(f"raio-{k}", r) for k, r in t["raios"].items()]
    v += [(f"sombra-{k}", s["valor"]) for k, s in t["sombras"].items()]
    f = t["efeitos"]
    v += [("neon-espessura", f"{f['neon-espessura-px']}px"), ("neon-brilho", f"{f['neon-brilho-px']}px"),
          ("painel-opacidade-min", str(f["painel-opacidade"][0])), ("painel-opacidade-max", str(f["painel-opacidade"][1])),
          ("menu-desfoque", f"{f['menu-desfoque-px']}px"), ("radio-inativo-opacidade", str(f["radio-inativo-opacidade"])),
          ("inimigo-mancha-opacidade", str(f["inimigo-mancha-opacidade"]))]
    linhas = "\n".join(f"  --cn-{k}: {val};" for k, val in v)
    return ("/* Costa Neon: gerado por `costa_neon.py tokens build` a partir do tokens.json. Não edite à mão. */\n"
            f":root {{\n{linhas}\n}}\n")


def construir(t: dict, destino: Path = ARQUIVO, checar: bool = False) -> bool:
    """Grava o CSS (ou, com checar, só diz se o arquivo está em dia). Devolve True se está em dia."""
    novo = gerar(t)
    atual = destino.read_text(encoding="utf-8") if destino.is_file() else None
    if checar:
        return atual == novo
    if atual != novo:
        destino.write_text(novo, encoding="utf-8", newline="\n")
    return True
