# feat-02-01-paleta-e-contraste — Paleta e contraste de letreiro

Iniciativa: `sdd/discovery/02-letreiro-neon/`. Branch: `feat/02-letreiro-neon`. Task 02-01 do plano.

## Objetivo
Acrescentar ao `tokens.json` as cores de letreiro com hex deslocados (ADR-0007): `lima-destaque`, `painel-letreiro` (fundo quase preto), `contorno-painel` (claro, exceção declarada), `rosa-letreiro` e o degradê `ceu-letreiro` (roxo, magenta, laranja, amarelo). Regra de uso: um lima por peça, só em valor ou oferta. `validar` aceita o contorno claro apenas no `painel-letreiro` e segue reprovando hex fora dos tokens. Teste de contraste por par texto/fundo.

## Modelo do módulo
`enxuto`: estende `tokens.json`, `tokens build` e `validar` da 01-01; novo `tests/test_contraste.py`.

## Decisões do projeto aplicadas
ADR-0001 (fonte única), ADR-0002 (contorno na tinta, exceção só declarada em token), ADR-0007 (hex deslocados). Regras 3, 4, 8.

## O que já existe
| Procurei | Onde | Achei | Decisão | Justificativa |
|---|---|---|---|---|
| Cores e degradês | `tokens/costa-neon.tokens.json` | `cores`, `degrades` | estender | `DUP-01` |
| Regra do contorno | `scripts/cn/validar.py` | contorno só `cor.tinta` | estender | exceção lida do token, sem lista solta |
| Contraste | — | nada | criar | função única de luminância WCAG, reusada por 02-02 e 02-04 |

## Dependências novas
Nenhuma.

## Rules e IDs da Constituição Aplicáveis
`DUP-01`, `DUP-04`, `TST-01`, `COD-02`; rule `sdd-reuso-e-duplicacao.md`.

## Critérios de Aceitação Executáveis
- `uv run costa_neon.py tokens build --checar` sai 0 (CSS em dia com as cores novas).
- `uv run pytest tests/test_validar.py tests/test_contraste.py` sai 0: hex lima fora dos tokens reprova; contorno claro só no `painel-letreiro`; todo par texto/fundo do letreiro >= 4,5:1 (título grande >= 3:1).
- `uv run costa_neon.py validar` sai 0; `uv run ruff check` sai 0.
