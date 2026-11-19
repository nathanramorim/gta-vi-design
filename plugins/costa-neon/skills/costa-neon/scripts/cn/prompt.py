"""prompt: monta o texto de cada um dos 6 modos a partir dos dados de ilustracao/ (ADR-0002)."""
from __future__ import annotations

import json
import random
from dataclasses import dataclass, field

from cn import entrada, termos
from cn.entrada import SKILL, ErroDados

PASTA = SKILL / "ilustracao"
SORTEIO = ("PESSOA", "ARQUETIPO", "IDADE", "CORPO", "CABELO", "ROUPA", "ACESSORIO", "POSE", "LUGAR", "HORA", "LADO")
TIPOS_ESCRITA = ("lettering", "rotulo", "sinopse", "menu", "dica", "descricao")


@dataclass
class Resultado:
    modo: int
    texto: str
    semente: int | None = None
    valores: dict = field(default_factory=dict)
    montagem: str | None = None
    avisos: list[str] = field(default_factory=list)


def _json(nome: str) -> dict:
    return json.loads((PASTA / nome).read_text(encoding="utf-8"))


def estilo() -> str:
    return (PASTA / "estilo.txt").read_text(encoding="utf-8").strip()


def limpar(nome: str, valor: str, maximo: int = 80) -> str:
    """Borda: tamanho, caracteres e nenhum nome de obra existente."""
    valor = entrada.texto(nome, valor, maximo)
    if termos.achar(valor):
        raise ErroDados(f"{nome}: tem nome de obra, marca ou fonte existente; use nomes inventados")
    return valor


def _preencher(modelo: str, valores: dict) -> str:
    for k, v in valores.items():
        modelo = modelo.replace("{" + k + "}", v)
    return modelo


def _sortear(semente: int, dados_fixos: dict) -> dict:
    rnd = random.Random(semente)
    listas = _json("listas.json")
    return {k: dados_fixos.get(k) or rnd.choice(listas[k]) for k in SORTEIO} | dados_fixos


def montar(modo: int, *, variaveis: dict, fixos: dict, semente: int | None = None, foto_autorizada: bool = False,
           tipo: str | None = None, tema: str | None = None, descricao: str | None = None, formato: str | None = None) -> Resultado:
    v = {k: limpar(k, val) for k, val in variaveis.items()}
    fixos = {k.upper(): limpar(k, val) for k, val in fixos.items() if val}
    if modo == 1:
        texto = ("Modo 1 — design system {SISTEMA}. Rode, nesta ordem: `tokens build` (CSS a partir do tokens.json), "
                 "`validar` (confere hex, sombras, contorno, barras e nomes), `tema todos --saida <pasta> --previa` "
                 "(um tema por ferramenta) e `prompt --modo 2..6` para as imagens. Marca: {MARCA}. Cidade: {CIDADE}. Idioma: {IDIOMA}.")
        return Resultado(1, _preencher(texto, v))
    if modo == 5:
        if tipo not in TIPOS_ESCRITA:
            raise ErroDados(f"modo 5 pede --tipo entre {', '.join(TIPOS_ESCRITA)}")
        return Resultado(5, _preencher(_json("escrita.json")[tipo], v))
    receitas = _json("receitas.json")
    semente = semente if semente is not None else random.SystemRandom().randrange(1, 10**6)
    avisos: list[str] = []
    montagem = None
    if modo == 2:
        if not foto_autorizada:
            raise ErroDados("modo 2 pede --foto-autorizada: a pessoa da foto autorizou, é adulta e não é figura pública (declaração dela, nunca da IA)")
        modelo = receitas["foto"]
        avisos.append("Use só foto com autorização da pessoa, adulta e que não seja figura pública.")
    elif modo == 3:
        modelo = receitas["aleatorio"]
    elif modo == 4:
        modelo = receitas["cenario"]
    elif modo == 6:
        temas = _json("tematica.json")
        if tema not in temas:
            raise ErroDados(f"modo 6 pede --tema entre {', '.join(temas)}")
        if not descricao:
            raise ErroDados("modo 6 pede --descricao (a cena, em poucas palavras)")
        fixos["TEMA"] = temas[tema]["tema"]
        fixos["DESCRICAO"] = limpar("descricao", descricao, 160)
        formato = formato or temas[tema]["formato"]
        montagem = _preencher(temas[tema]["montagem"], v) + " Texto e interface entram depois, na montagem; a imagem vem sem texto."
        modelo = receitas["tematica"]
    else:
        raise ErroDados("modo deve ser de 1 a 6")
    valores = _sortear(semente, fixos)
    valores["CIDADE"] = v["CIDADE"]
    valores["FORMATO"] = entrada.formato(formato or v["FORMATO"])
    texto = estilo() + "\n" + _preencher(modelo, valores)
    usados = {k: valores[k] for k in valores if "{" + k + "}" in modelo}
    return Resultado(modo, texto, semente, usados, montagem, avisos)
