"""tema: cada consumidor recebe o formato que já lê, com valores dos tokens; só a --saida é escrita."""
import importlib.util
import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from cn import banner, logo, temas, validar
from cn import tokens as tk
from conftest import RAIZ


def _repo(var: str, nome: str) -> Path:
    """Clone do consumidor: variável de ambiente ou, por padrão, ~/git/<nome>."""
    return Path(os.environ.get(var) or Path.home() / "git" / nome)


CARROSSEL = _repo("COSTA_NEON_CARROSSEL", "carrossel-studio") / "plugins" / "carrossel-studio" / "skills" / "gerar-carrossel" / "scripts" / "marca.py"
README_EXEMPLO = _repo("COSTA_NEON_README_STUDIO", "readme-studio") / "exemplos" / "forge-sdd" / "identidade.json"
GERADOR = _repo("COSTA_NEON_GERADOR_VIDEOS", "gerador-videos") / "src"


def test_todos_os_temas_e_previas(cli, tmp_path):
    r = cli("tema", "todos", "--saida", str(tmp_path), "--previa", "--json")
    assert r.returncode == 0, r.stderr
    nomes = {Path(p).relative_to(tmp_path).as_posix() for p in json.loads(r.stdout)["arquivos"]}
    assert {"marca.json", "conteudo/.video-marca.json", "conteudo/marca/logo.svg", "identidade.json", "logo.svg.frag", "ilustracao.svg.frag", "forge-sdd-missoes.json", "logo.svg",
            "marca/logo.svg", "previa-forge-sdd.svg"} <= nomes
    assert not validar.validar([tmp_path], tk.carregar()), "tema gerado com algo fora do Costa Neon"


def test_marca_usa_os_tokens(tokens):
    m = temas.marca(tokens)
    assert set(m["cores"]) == {"bg", "surface", "text", "muted", "accent", "accent2", "success", "danger"}
    assert set(m["cores"].values()) <= tk.hex_permitidos(tokens)
    assert m["fontes"]["title"] == "Oswald"


def test_pesos_que_o_carrossel_pede_existem(tokens):
    pesos = {f["fonte"]: set(f["pesos"]) for f in tokens["tipografia"]["familias"].values()}
    m = temas.marca(tokens)["fontes"]
    assert {400, 500, 600} <= pesos[m["title"]]
    assert {400, 500} <= pesos[m["body"]] and {400, 500} <= pesos[m["mono"]]


@pytest.mark.skipif(not CARROSSEL.is_file(), reason="carrossel-studio não está em ~/git nesta máquina")
def test_carrossel_aceita_o_arquivo_de_marca(tmp_path, tokens):
    temas.gerar("carrossel", tokens, tmp_path, False, gravar=True)
    spec = importlib.util.spec_from_file_location("marca_carrossel", CARROSSEL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    m = mod.carregar_marca(tmp_path)
    assert m["_logo"] is not None


LER_VIDEO = (
    "import json, sys; from pathlib import Path; "
    "from gerador_videos.motor.marca import override; from gerador_videos.motor.marca.projeto import Projeto; "
    "a = override.detectar(Projeto(Path(sys.argv[1]))); print(json.dumps({'cores': a.cores, 'fontes': a.fontes, 'logo': a.logo}))"
)


@pytest.mark.skipif(not (GERADOR / "gerador_videos").is_dir() or not shutil.which("uv"),
                    reason="gerador-videos ou uv não estão nesta máquina (COSTA_NEON_GERADOR_VIDEOS)")
def test_gerador_videos_le_cores_fontes_e_logo(tmp_path, tokens):
    """Roda o leitor de marca do gerador-videos no ambiente dele (as dependências dele não entram aqui)."""
    temas.gerar("video", tokens, tmp_path, False, gravar=True)
    r = subprocess.run(["uv", "run", "--directory", str(GERADOR.parent), "python", "-c", LER_VIDEO, str(tmp_path)],
                       capture_output=True, text=True, encoding="utf-8", timeout=300)
    assert r.returncode == 0, r.stderr
    achado = json.loads(r.stdout.strip().splitlines()[-1])
    assert achado["logo"] == "conteudo/marca/logo.svg"
    assert {k: v.upper() for k, v in achado["cores"].items()} == {k: v.upper() for k, v in temas.marca(tokens)["cores"].items()}
    assert set(achado["fontes"]) == {"title", "body", "mono"}


@pytest.mark.skipif(not README_EXEMPLO.is_file(), reason="readme-studio não está em ~/git nesta máquina")
def test_identidade_tem_as_chaves_do_readme_studio(tokens):
    exemplo = json.loads(README_EXEMPLO.read_text(encoding="utf-8"))
    assert set(temas.identidade(tokens)) == set(exemplo)


def test_forge_sdd_tem_5_missoes(tokens):
    f = temas.forge_sdd(tokens)
    assert [m["n"] for m in f["missoes"]] == [1, 2, 3, 4, 5]
    assert f["fontes"]["display"] == "Bowlby One"
    assert {m["cor"] for m in f["missoes"]} <= tk.hex_permitidos(tokens)


def test_validar_nao_grava(cli, tmp_path):
    r = cli("tema", "readme", "--saida", str(tmp_path / "x"), "--validar")
    assert r.returncode == 0 and not (tmp_path / "x").exists()


def test_saida_que_e_arquivo_sai_2(cli, tmp_path):
    arq = tmp_path / "arquivo.txt"
    arq.write_text("x", encoding="utf-8")
    assert cli("tema", "carrossel", "--saida", str(arq)).returncode == 2


def test_banner_do_readme_usa_o_tema(tokens):
    d = RAIZ / "docs" / "img"
    assert json.loads((d / "identidade.json").read_text(encoding="utf-8")) == temas.identidade(tokens)
    assert (d / "logo.svg.frag").read_text(encoding="utf-8") == logo.fragmento(tokens) + "\n"
    assert (d / "ilustracao.svg.frag").read_text(encoding="utf-8") == banner.ilustracao(tokens)
