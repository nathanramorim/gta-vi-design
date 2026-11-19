import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
SKILL = RAIZ / "plugins" / "costa-neon" / "skills" / "costa-neon"
CLI = SKILL / "scripts" / "costa_neon.py"
DADOS = Path(__file__).resolve().parent / "dados"
sys.path.insert(0, str(SKILL / "scripts"))


def rodar(*args: str, cwd: Path = RAIZ) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(CLI), *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8")


@pytest.fixture
def cli():
    return rodar


@pytest.fixture(scope="session")
def tokens():
    from cn import tokens as tk
    return tk.carregar()
