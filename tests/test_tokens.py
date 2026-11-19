"""tokens build: CSS gerado e em dia (ADR-0001)."""
from cn import css


def test_css_em_dia(tokens):
    assert css.ARQUIVO.read_text(encoding="utf-8") == css.gerar(tokens)


def test_uma_variavel_por_cor_e_degrade(tokens):
    texto = css.gerar(tokens)
    for k in tokens["cores"]:
        assert f"--cn-cor-{k}:" in texto
    for k in tokens["degrades"]:
        assert f"--cn-degrade-{k}: linear-gradient(" in texto


def test_checar_nao_grava(tmp_path, tokens):
    destino = tmp_path / "x.css"
    destino.write_text("velho", encoding="utf-8")
    assert css.construir(tokens, destino, checar=True) is False
    assert destino.read_text(encoding="utf-8") == "velho"
    assert css.construir(tokens, destino) is True
    assert css.construir(tokens, destino, checar=True) is True


def test_cli_checar(cli):
    r = cli("tokens", "build", "--checar")
    assert r.returncode == 0, r.stderr
