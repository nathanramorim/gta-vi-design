"""Termos bloqueados (nomes de obras, marcas e fontes existentes) guardados só como SHA-256 (ADR-0002)."""
from __future__ import annotations

import hashlib
import re
import unicodedata

from cn.entrada import SKILL

ARQUIVO = SKILL / "dados" / "termos-bloqueados.txt"
MAX_PALAVRAS = 4


def normalizar(texto: str) -> list[str]:
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.findall(r"[a-z0-9]+", sem_acento.lower())


def resumo(termo: str) -> str:
    return hashlib.sha256(" ".join(normalizar(termo)).encode()).hexdigest()


def carregar() -> set[str]:
    linhas = ARQUIVO.read_text(encoding="utf-8").splitlines()
    return {s.strip() for s in linhas if s.strip() and not s.startswith("#")}


def achar(texto: str, bloqueados: set[str] | None = None) -> bool:
    """True se algum trecho de 1 a 4 palavras do texto está na lista."""
    hashes = carregar() if bloqueados is None else bloqueados
    palavras = normalizar(texto)
    for n in range(1, MAX_PALAVRAS + 1):
        for i in range(len(palavras) - n + 1):
            if hashlib.sha256(" ".join(palavras[i:i + n]).encode()).hexdigest() in hashes:
                return True
    return False
