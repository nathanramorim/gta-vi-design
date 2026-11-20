"""Fontes abertas do fontsource, baixadas uma vez para o cache (Regra 11, SEG-07)."""
from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

from cn.entrada import ErroDados

API = "https://api.fontsource.org/v1/fonts/"
LICENCAS_ABERTAS = ("OFL-1.1", "Apache-2.0")
HOSTS = ("https://cdn.jsdelivr.net/",)


def cache() -> Path:
    return Path(os.environ.get("COSTA_NEON_CACHE") or Path.home() / ".cache" / "costa-neon" / "fontes")


def _ler(url: str) -> bytes:
    if not url.startswith(("https://api.fontsource.org/", *HOSTS)):
        raise ErroDados(f"fonte: endereço fora do fontsource: {url}")
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "costa-neon"}), timeout=30) as r:  # noqa: S310 (https e hosts conferidos acima)
            return r.read()
    except OSError as e:
        raise ErroDados(f"fonte: não consegui baixar {url} ({e})") from e


def metadados(fontsource: str) -> dict:
    return json.loads(_ler(API + fontsource))


def arquivo(fontsource: str, peso: int) -> Path:
    """Caminho do woff2 latino no cache; baixa uma vez, depois de conferir a licença na API."""
    destino = cache() / f"{fontsource}-{peso}.woff2"
    if destino.is_file():
        return destino
    meta = metadados(fontsource)
    if meta["license"] not in LICENCAS_ABERTAS:
        raise ErroDados(f"fonte {fontsource}: licença {meta['license']} não é aberta (OFL ou Apache)")
    try:
        url = meta["variants"][str(peso)]["normal"]["latin"]["url"]["woff2"]
    except KeyError as e:
        raise ErroDados(f"fonte {fontsource}: peso {peso} não existe") from e
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(_ler(url))
    return destino


def face_css(t: dict, familia: str) -> str:
    """@font-face de cada peso da família dos tokens, apontando para o cache (file://)."""
    f = t["tipografia"]["familias"][familia]
    return "\n".join(f"@font-face {{ font-family: '{f['fonte']}'; font-weight: {p}; src: url('{arquivo(f['fontsource'], p).as_uri()}') format('woff2'); }}"
                     for p in f["pesos"])
