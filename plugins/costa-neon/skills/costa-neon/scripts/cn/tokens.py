"""Leitura do tokens.json (ADR-0001) e a lista de hex permitidos (ADR-0007)."""
from __future__ import annotations

import json
from pathlib import Path

from cn.entrada import RE_HEX, SKILL, ErroDados

ARQUIVO = SKILL / "tokens" / "costa-neon.tokens.json"


def carregar(caminho: Path | None = None) -> dict:
    arq = caminho or ARQUIVO
    try:
        dado = json.loads(arq.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise ErroDados(f"{arq}: não consegui ler os tokens ({e})") from e
    if not isinstance(dado, dict) or not isinstance(dado.get("cores"), dict) or not isinstance(dado.get("degrades"), dict):
        raise ErroDados(f"{arq}: faltam 'cores' ou 'degrades'")
    return dado


def cor(t: dict, nome: str) -> str:
    return t["cores"][nome]["valor"]


def paradas(t: dict, nome: str) -> list[str]:
    return list(t["degrades"][nome]["paradas"])


def hex_permitidos(t: dict) -> set[str]:
    """Todo hex que aparece no tokens.json, em maiúsculas."""
    return {h.upper() for h in RE_HEX.findall(json.dumps(t))}


def degrade_css(t: dict, nome: str) -> str:
    d = t["degrades"][nome]
    p = d["paradas"]
    passos = ", ".join(f"{h} {round(i * 100 / (len(p) - 1))}%" for i, h in enumerate(p))
    return f"linear-gradient({d['angulo']}, {passos})"
