# ADR-0003: Python sempre via uv, em macOS, Linux e Windows

- **Data:** 2026-11-19
- **Status:** `aprovado`
- **Regras afetadas (IDs da constitution):** `ARQ-04`, `COD-02`, `SEG-03`, Regra 9
- **Autor / Responsável:** dono do repositório

## Contexto
Os scripts rodam na máquina de quem usa o design system, em qualquer sistema. pip e venv manual quebram e poluem o ambiente.

## Opções Consideradas
1. **pip + requirements.txt:** frágil.
2. **uv com PEP 723 nos scripts e `pyproject.toml` para dev:** um comando.

## Decisão
Opção 2. Caminhos com `pathlib`, processos sem shell, nada de caminho fixo. O README mostra o bootstrap por sistema (`bootstrap.sh` e `bootstrap.ps1`).

## Consequências
- **Positivas:** roda igual nos 3 sistemas.
- **Negativas / Trade-offs:** exige `uv` (o bootstrap instala).
- **Ações de acompanhamento:** CI em macOS, Linux e Windows quando houver código (feature 01).
