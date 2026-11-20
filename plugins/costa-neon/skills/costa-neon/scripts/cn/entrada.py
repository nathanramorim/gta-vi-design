"""Borda: erros de dado, caminhos da skill e validação de entrada (SEG-01)."""
from __future__ import annotations

import re
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2]
HEX = r"#[0-9A-Fa-f]{6}"  # padrão único do hex de 6 dígitos (DUP-04)
RE_HEX = re.compile(HEX)
RE_TEXTO = re.compile(r"[\w ,.'’:()/&-]*")
FORMATOS = ("16:9", "1:1", "9:16", "4:5")


class ErroDados(Exception):
    """Dado de entrada inválido (código de saída 2)."""


def texto(nome: str, valor: str, maximo: int = 80) -> str:
    """Variável livre: tamanho e caracteres limitados (sem marcação nem chaves)."""
    valor = " ".join(str(valor).split())
    if not valor or len(valor) > maximo or not RE_TEXTO.fullmatch(valor):
        raise ErroDados(f"{nome}: use até {maximo} caracteres, só letras, números, espaço e , . ' : ( ) / & -")
    return valor


def formato(valor: str) -> str:
    if valor not in FORMATOS:
        raise ErroDados(f"formato deve ser um de {', '.join(FORMATOS)} (veio {valor!r})")
    return valor


def pasta_saida(valor: str) -> Path:
    """Pasta de saída: pode não existir; nunca um arquivo."""
    p = Path(valor).expanduser()
    if p.exists() and not p.is_dir():
        raise ErroDados(f"--saida deve ser uma pasta: {p}")
    return p
