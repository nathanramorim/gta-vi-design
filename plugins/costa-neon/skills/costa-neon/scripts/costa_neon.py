#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Costa Neon: ferramentas determinísticas do design system (a IA chama, não inventa).

Uso:
  uv run costa_neon.py tokens build [--checar]
  uv run costa_neon.py validar [caminhos...] [--json]
  uv run costa_neon.py tema carrossel|video|readme|forge-sdd|todos --saida <pasta> [--previa] [--validar] [--json]
  uv run costa_neon.py render amostra --saida <pasta> [--linha1 X] [--linha2 Y] [--json]
  uv run costa_neon.py prompt --modo 1..6 | --cena letreiro [--semente N] [--formato 16:9|1:1|9:16] [--marca X] [--cidade Y] [--json]

Códigos: 0 ok; 1 CSS desatualizado (--checar); 2 dado inválido ou problema encontrado.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cn import css, entrada, letreiro, prompt, render, temas, validar  # noqa: E402
from cn import tokens as tk  # noqa: E402
from cn.entrada import ErroDados, pasta_saida  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def cmd_tokens(a: argparse.Namespace) -> int:
    t = tk.carregar()
    em_dia = css.construir(t, checar=a.checar)
    if a.checar and not em_dia:
        print("costa-neon.css desatualizado: rode `tokens build`", file=sys.stderr)
        return 1
    print("ok: costa-neon.css em dia" if a.checar else f"ok: {css.ARQUIVO.name}")
    return 0


def cmd_validar(a: argparse.Namespace) -> int:
    alvos = [Path(c) for c in a.caminhos] if a.caminhos else [Path(c) for c in validar.ALVOS_PADRAO if Path(c).exists()]
    faltando = [str(c) for c in alvos if not c.exists()]
    if faltando:
        raise ErroDados(f"caminho não existe: {', '.join(faltando)}")
    problemas = validar.validar(alvos, tk.carregar())
    if a.json:
        print(json.dumps({"ok": not problemas, "problemas": [p.__dict__ for p in problemas]}, ensure_ascii=False))
    else:
        for p in problemas:
            print(p.texto())
        print("ok: nada fora do Costa Neon" if not problemas else f"{len(problemas)} problema(s)")
    return 2 if problemas else 0


def cmd_prompt(a: argparse.Namespace) -> int:
    var = tk.carregar()["variaveis"]
    variaveis = {"SISTEMA": var["SISTEMA"], "MARCA": a.marca or var["MARCA"], "CIDADE": a.cidade or var["CIDADE"],
                 "IDIOMA": a.idioma or var["IDIOMA"], "FORMATO": var["FORMATO"]}
    fixos = {k: getattr(a, k) for k in ("pose", "roupa", "lugar", "hora", "lado", "arquetipo", "idade", "corpo", "cabelo", "acessorio", "pessoa")}
    if a.cena:
        if a.modo is not None:
            raise ErroDados("use --cena ou --modo, não os dois")
        r = prompt.montar_cena(a.cena, variaveis=variaveis, semente=a.semente, formato=a.formato)
        return _saida_prompt(a, r)
    if a.modo is None:
        raise ErroDados("informe --modo (1 a 6) ou --cena letreiro")
    r = prompt.montar(a.modo, variaveis=variaveis, fixos=fixos, semente=a.semente, foto_autorizada=a.foto_autorizada,
                      tipo=a.tipo, tema=a.tema, descricao=a.descricao, formato=a.formato)
    return _saida_prompt(a, r)


def _saida_prompt(a: argparse.Namespace, r: prompt.Resultado) -> int:
    if a.json:
        print(json.dumps({"ok": True, **r.__dict__}, ensure_ascii=False))
        return 0
    print(r.texto)
    for nota in ([f"semente: {r.semente}"] if r.semente is not None else []) + ([f"montagem: {r.montagem}"] if r.montagem else []) + r.avisos:
        print(nota, file=sys.stderr)
    return 0


def cmd_tema(a: argparse.Namespace) -> int:
    t = tk.carregar()
    saida = pasta_saida(a.saida)
    lista = temas.CONSUMIDORES if a.consumidor == "todos" else (a.consumidor,)
    feitos = [str(p) for c in lista for p in temas.gerar(c, t, saida, a.previa, gravar=not a.validar)]
    if a.json:
        print(json.dumps({"ok": True, "validar": a.validar, "arquivos": feitos}, ensure_ascii=False))
    else:
        print(("seria gravado:\n" if a.validar else "ok:\n") + "\n".join(feitos))
    return 0


def cmd_render(a: argparse.Namespace) -> int:
    t = tk.carregar()
    saida = pasta_saida(a.saida)
    l1, l2 = entrada.texto("linha1", a.linha1, 24), entrada.texto("linha2", a.linha2, 24)
    html, png = saida / "amostra-letreiro.html", saida / "amostra-letreiro.png"
    saida.mkdir(parents=True, exist_ok=True)
    html.write_text(letreiro.amostra(t, l1, l2), encoding="utf-8", newline="\n")
    tamanho = render.png(html, png, 1080, 640)
    if a.json:
        print(json.dumps({"ok": True, "png": str(png), "tamanho": tamanho}, ensure_ascii=False))
    else:
        print(f"ok: {png} {tamanho[0]}x{tamanho[1]}")
    return 0


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="costa_neon.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="comando", required=True)
    p = sub.add_parser("tokens", help="gera o CSS a partir do tokens.json")
    p.add_argument("acao", choices=["build"])
    p.add_argument("--checar", action="store_true", help="só confere se o CSS está em dia (não grava)")
    p.set_defaults(func=cmd_tokens)
    p = sub.add_parser("validar", help="confere os artefatos contra os tokens e as regras")
    p.add_argument("caminhos", nargs="*")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_validar)
    p = sub.add_parser("tema", help="gera o tema de uma ferramenta consumidora")
    p.add_argument("consumidor", choices=[*temas.CONSUMIDORES, "todos"])
    p.add_argument("--saida", required=True, help="pasta de saída (só ela é escrita; os arquivos do tema são sobrescritos). Para video, a raiz do projeto")
    p.add_argument("--previa", action="store_true", help="grava também previa-<consumidor>.svg para conferência visual")
    p.add_argument("--validar", action="store_true", help="só lista o que seria gravado")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_tema)
    p = sub.add_parser("render", help="renderiza uma página HTML dos tokens em PNG no Chrome local")
    p.add_argument("alvo", choices=["amostra"])
    p.add_argument("--saida", required=True, help="pasta de saída (só ela é escrita)")
    p.add_argument("--linha1", default="Nova missão")
    p.add_argument("--linha2", default="desbloqueada")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_render)
    p = sub.add_parser("prompt", help="monta o prompt de imagem ou o roteiro de texto (6 modos)")
    p.add_argument("--modo", type=int, choices=range(1, 7))
    p.add_argument("--cena", help="fundo de peça sem texto: letreiro (no lugar de --modo)")
    p.add_argument("--semente", type=int)
    p.add_argument("--formato")
    for nome in ("marca", "cidade", "idioma", "pose", "roupa", "lugar", "hora", "lado", "arquetipo", "idade", "corpo", "cabelo", "acessorio", "pessoa"):
        p.add_argument(f"--{nome}")
    p.add_argument("--foto-autorizada", action="store_true", help="modo 2: a pessoa da foto autorizou, é adulta e não é figura pública")
    p.add_argument("--tipo", help="modo 5: lettering, rotulo, sinopse, menu, dica ou descricao")
    p.add_argument("--tema", help="modo 6: loading, capa, post, story, divisor ou encerramento")
    p.add_argument("--descricao", help="modo 6: a cena")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_prompt)
    return ap


def main(argv: list[str] | None = None) -> int:
    a = parser().parse_args(argv)
    try:
        return a.func(a)
    except ErroDados as e:
        if getattr(a, "json", False):
            print(json.dumps({"ok": False, "codigo": 2, "erro": str(e)}, ensure_ascii=False))
        else:
            print(f"erro: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
