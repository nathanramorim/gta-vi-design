# feat-01-01-tokens-e-validar — Tokens (paleta deslocada), tokens build e validar

Iniciativa: `sdd/discovery/01-costa-neon/`. Branch: `feat/01-costa-neon`. Feature 01 do plano.

## Objetivo
`plugins/costa-neon/skills/costa-neon/tokens/costa-neon.tokens.json` como fonte única (62 hex deslocados, ADR-0007), `tokens build` gerando `costa-neon.css` (uma variável por token, `--checar` para CI), e `validar` com as 5 checagens: hex fora dos tokens, preto puro, sombra que não seja roxa ou azul (brilho `0 0 Npx` é livre), contorno que não seja a tinta, tela sem barras e linha neon, e termos bloqueados (hash SHA-256 de n-gramas). CI em Linux, Windows e macOS.

## Modelo do módulo
`enxuto`: CLI fina (`scripts/costa_neon.py`) + módulos irmãos em `scripts/cn/` (`tokens.py`, `css.py`, `validar.py`, `termos.py`, `entrada.py`), só biblioteca padrão, sem estado.

## Decisões do projeto aplicadas
ADR-0001 (fonte única), ADR-0002 (Pricedown e nomes bloqueados), ADR-0003 (uv, pathlib, sem shell), ADR-0005 (motor dentro da skill), ADR-0007 (paleta deslocada). Regras 3, 4, 8, 9, 10, 15.

## O que já existe
| Procurei | Onde | Achei | Decisão | Justificativa |
|---|---|---|---|---|
| Tokens do tema 5.0 | forge-sdd `feat/readme-v5-gta-vi` | tokens medidos de conceito de terceiros | não reusar | ADR-0002/0007; só os valores entram em `tests/dados/evitar-hex.txt` para o teste de distância |
| Validação de cor na borda | carrossel-studio `marca.py` (`RE_COR`) | regex `#RRGGBB` | reusar o padrão | mesma regra de entrada |
| Layout de plugin com motor na skill | carrossel-studio `plugins/carrossel-studio/skills/gerar-carrossel/` | scripts dentro da skill | reusar o padrão | plugin instalado funciona sozinho |

## Dependências novas
Nenhuma de runtime. Dev: `pytest`, `ruff` (grupo `dev` do `pyproject.toml`).

## Rules e IDs da Constituição Aplicáveis
`DUP-04`, `TST-01`, `TST-03`, `TST-04`, `COD-02`, `SEG-01`, `SEG-02`, `SEG-03`, `ARQ-05`, `ARQ-06`; rules `sdd-arquitetura.md`, `sdd-codigo-e-testes.md`, `sdd-seguranca.md`, `sdd-reuso-e-duplicacao.md`.

## Critérios de Aceitação Executáveis
- `uv run ruff check` sai 0.
- `uv run pytest tests/test_paleta.py tests/test_tokens.py tests/test_validar.py` sai 0: 62 hex, todos fora de ±3 do conceito e do prompt; CSS em dia; cada fixture ruim sai 2; os artefatos oficiais saem 0.
- `uv run plugins/costa-neon/skills/costa-neon/scripts/costa_neon.py tokens build --checar` sai 0.
- `uv run plugins/costa-neon/skills/costa-neon/scripts/costa_neon.py validar` sai 0 na raiz do repositório.
