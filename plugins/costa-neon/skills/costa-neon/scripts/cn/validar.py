"""validar: confere os artefatos contra os tokens e as regras do Costa Neon (regras 4 e 8).

Checagens: hex fora do tokens.json, preto puro, sombra que não é roxa ou azul (brilho `0 0 Npx` é livre),
contorno que não é a tinta, tela sem barras e linha neon, e termo bloqueado (nome de obra existente).
"""
from __future__ import annotations

import colorsys
import re
from dataclasses import dataclass
from pathlib import Path

from cn import termos
from cn import tokens as tk

ALVOS_PADRAO = ("tokens", "fundamentos", "componentes", "telas", "ilustracao", "temas", "plugins", "README.md")
EXTENSOES = {".css", ".html", ".svg", ".json", ".md", ".txt", ".frag", ".py"}
IGNORAR_PASTAS = {".git", "__pycache__", ".venv", "node_modules", "sdd"}
IGNORAR_ARQUIVOS = {"prompt-diretor-de-arte.md", "termos-bloqueados.txt"}
VISUAIS = {".css", ".html", ".svg"}

RE_HEX6 = re.compile(r"(?<![\w&])#([0-9A-Fa-f]{6})\b")
RE_HEX3 = re.compile(r"(?<![\w&])#([0-9A-Fa-f]{3})\b")
RE_RGB = re.compile(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})")
RE_PRETO = re.compile(r"(?::\s*|=\s*\")black\b|rgba?\(\s*0\s*,\s*0\s*,\s*0\b", re.IGNORECASE)
RE_SOMBRA = re.compile(r"(?:box-shadow|text-shadow)\s*:\s*([^;}\"]+)|drop-shadow\(((?:[^()]|\([^()]*\))*)\)", re.IGNORECASE)
RE_STROKE_TEXTO = re.compile(r"-webkit-text-stroke(?:-color)?\s*:\s*([^;}\"]+)", re.IGNORECASE)
RE_STROKE_SVG = re.compile(r"\bstroke\s*[=:]\s*\"?\s*(#[0-9A-Fa-f]{6}|rgba?\([^)]*\))", re.IGNORECASE)
RE_SOMBRA_JSON = re.compile(r"\"sombras\"\s*:\s*\{(.*?)\n\s{0,4}\}", re.DOTALL)


@dataclass
class Problema:
    arquivo: str
    linha: int
    regra: str
    detalhe: str

    def texto(self) -> str:
        return f"{self.arquivo}:{self.linha}: [{self.regra}] {self.detalhe}"


def _rgb(cor: str) -> tuple[int, int, int] | None:
    cor = cor.strip()
    if m := re.fullmatch(r"#([0-9A-Fa-f]{6})", cor):
        h = m.group(1)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]
    if m := RE_RGB.search(cor):
        return tuple(int(x) for x in m.groups())  # type: ignore[return-value]
    return None


def roxa_ou_azul(rgb: tuple[int, int, int]) -> bool:
    h, luz, s = colorsys.rgb_to_hls(*(x / 255 for x in rgb))
    return 200 <= h * 360 <= 340 and s >= 0.15


def _camadas(valor: str) -> list[str]:
    partes, nivel, atual = [], 0, ""
    for ch in valor:
        nivel += (ch == "(") - (ch == ")")
        if ch == "," and nivel == 0:
            partes.append(atual)
            atual = ""
        else:
            atual += ch
    return [p.strip() for p in partes + [atual] if p.strip()]


def _sombra(camada: str) -> str | None:
    """None se a camada está ok; senão o motivo."""
    cor = re.search(r"#[0-9A-Fa-f]{6}|rgba?\([^)]*\)", camada)
    numeros = re.findall(r"(-?\d*\.?\d+)(?:px)?\b", RE_RGB.sub("", re.sub(r"#[0-9A-Fa-f]{6}", "", camada)))
    if len(numeros) >= 2 and float(numeros[0]) == 0 and float(numeros[1]) == 0:
        return None  # brilho centrado (neon), na mesma cor
    if not cor:
        return f"sombra sem cor explícita: {camada!r}"
    rgb = _rgb(cor.group(0))
    if rgb is None or not roxa_ou_azul(rgb):
        return f"sombra deve ser roxa ou azul: {camada!r}"
    return None


def _linha(texto: str, pos: int) -> int:
    return texto.count("\n", 0, pos) + 1


def conferir_texto(nome: str, texto: str, sufixo: str, t: dict, permitidos: set[str], bloqueados: set[str]) -> list[Problema]:
    out: list[Problema] = []
    tinta = tk.cor(t, "tinta").upper()
    add = lambda pos, regra, det: out.append(Problema(nome, _linha(texto, pos), regra, det))  # noqa: E731
    for m in RE_HEX6.finditer(texto):
        h = "#" + m.group(1).upper()
        if not h.strip("#0"):
            add(m.start(), "preto", "preto puro é proibido; use a tinta ou o preto de barra dos tokens")
        elif h not in permitidos:
            add(m.start(), "hex", f"{h} não está no tokens.json")
    if sufixo != ".md":
        for m in RE_HEX3.finditer(texto):
            add(m.start(), "hex", f"#{m.group(1)}: use o hex de 6 dígitos de um token")
    if sufixo in VISUAIS:
        for m in RE_PRETO.finditer(texto):
            add(m.start(), "preto", "preto puro é proibido")
    if sufixo in VISUAIS | {".json"}:
        blocos = [(m.start(), m.group(1) or m.group(2)) for m in RE_SOMBRA.finditer(texto)]
        for mj in RE_SOMBRA_JSON.finditer(texto) if sufixo == ".json" else []:
            blocos += [(mj.start() + v.start(), v.group(1)) for v in re.finditer(r"\"valor\"\s*:\s*\"([^\"]+)\"", mj.group(1))]
        for pos, valor in blocos:
            for camada in _camadas(valor):
                if motivo := _sombra(camada):
                    add(pos, "sombra", motivo)
        for m in RE_STROKE_TEXTO.finditer(texto):
            cor = re.search(r"#[0-9A-Fa-f]{6}", m.group(1))
            if not cor or cor.group(0).upper() != tinta:
                add(m.start(), "contorno", f"contorno de texto deve ser a tinta {tinta}")
        for m in RE_STROKE_SVG.finditer(texto):
            rgb = _rgb(m.group(1))
            if rgb and colorsys.rgb_to_hls(*(x / 255 for x in rgb))[1] < 0.2 and m.group(1).upper() != tinta:
                add(m.start(), "contorno", f"contorno escuro deve ser a tinta {tinta}")
    if sufixo == ".html" and "telas" in Path(nome).parts:
        if "cn-barra-topo" not in texto or "cn-barra-base" not in texto:
            add(0, "tela", "tela sem as barras de topo e base (cn-barra-topo, cn-barra-base)")
        if texto.count("cn-linha-neon") < 2:
            add(0, "tela", "tela sem a linha neon nas duas barras (cn-linha-neon)")
    for i, linha in enumerate(texto.splitlines(), 1):
        if termos.achar(linha, bloqueados):
            out.append(Problema(nome, i, "termo", "nome de obra, marca ou fonte existente (ADR-0002)"))
    return out


def arquivos(alvos: list[Path]) -> list[Path]:
    achados: list[Path] = []
    for alvo in alvos:
        itens = [alvo] if alvo.is_file() else sorted(alvo.rglob("*"))
        for p in itens:
            if p.is_file() and p.suffix in EXTENSOES and p.name not in IGNORAR_ARQUIVOS \
                    and not IGNORAR_PASTAS.intersection(p.parts):
                achados.append(p)
    return achados


def validar(alvos: list[Path], t: dict) -> list[Problema]:
    permitidos = tk.hex_permitidos(t)
    bloqueados = termos.carregar()
    out: list[Problema] = []
    for p in arquivos(alvos):
        try:
            texto = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        out += conferir_texto(p.as_posix(), texto, p.suffix, t, permitidos, bloqueados)
    return out
