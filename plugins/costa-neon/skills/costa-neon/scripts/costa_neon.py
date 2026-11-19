#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Costa Neon: ferramentas determinísticas do design system (a IA chama, não inventa).

Uso:
  uv run costa_neon.py tokens build [--checar]
  uv run costa_neon.py validar [caminhos...] [--json]

Códigos: 0 ok; 1 CSS desatualizado (--checar); 2 dado inválido ou problema encontrado.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cn import css, validar  # noqa: E402
from cn import tokens as tk  # noqa: E402
from cn.entrada import ErroDados  # noqa: E402

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
