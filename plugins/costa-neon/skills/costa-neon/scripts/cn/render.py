"""HTML -> PNG no Chrome local (ADR-0004), sem dependência de runtime: o tamanho do PNG é lido do cabeçalho."""
from __future__ import annotations

import os
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

from cn.entrada import ErroDados

CANDIDATOS = {
    "darwin": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/Applications/Chromium.app/Contents/MacOS/Chromium"],
    "linux": ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser"],
    "win32": [r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"],
}


def chrome() -> str | None:
    """Variável COSTA_NEON_CHROME, depois os candidatos do sistema; None se não houver."""
    if env := os.environ.get("COSTA_NEON_CHROME"):
        return env if Path(env).is_file() else None
    for c in CANDIDATOS.get(sys.platform, CANDIDATOS["linux"]):
        if achado := (c if Path(c).is_file() else shutil.which(c)):
            return achado
    return None


def tamanho_png(arquivo: Path) -> tuple[int, int]:
    b = arquivo.read_bytes()[:24]
    if b[:8] != b"\x89PNG\r\n\x1a\n":
        raise ErroDados(f"{arquivo}: não é um PNG")
    return struct.unpack(">II", b[16:24])


def png(html: Path, destino: Path, largura: int, altura: int) -> tuple[int, int]:
    """Renderiza o HTML em `destino` (PNG) e devolve o tamanho conferido."""
    exe = chrome()
    if not exe:
        raise ErroDados("Chrome não encontrado: instale o Chrome ou aponte COSTA_NEON_CHROME para o executável")
    destino.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as perfil:
        r = subprocess.run([exe, "--headless=new", "--disable-gpu", "--no-sandbox", f"--user-data-dir={perfil}", "--hide-scrollbars",
                            "--force-device-scale-factor=1", f"--window-size={largura},{altura}", "--virtual-time-budget=4000",
                            f"--screenshot={destino}", html.resolve().as_uri()], capture_output=True, text=True, timeout=90)
    if r.returncode != 0 or not destino.is_file():
        raise ErroDados(f"render falhou: {r.stderr.strip()[-300:]}")
    return tamanho_png(destino)
