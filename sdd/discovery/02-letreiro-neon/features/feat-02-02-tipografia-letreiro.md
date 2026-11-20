# feat-02-02-tipografia-letreiro — Tipografia de letreiro

Iniciativa: `sdd/discovery/02-letreiro-neon/`. Branch: `feat/02-letreiro-neon`. Task 02-02 do plano.

## Objetivo
Escolher e registrar a fonte display condensada de peso máximo (candidatas: Anton, Barlow Condensed, League Gothic) e uma sans de corpo, ambas OFL ou Apache, conferidas na API do fontsource. Estilo `titulo-letreiro` nos tokens: contorno `cor.tinta` de 3 a 4px, sombra dura roxa, inclinação leve, linha 1 branca e linha 2 `rosa-letreiro`. Pricedown e similares seguem barradas.

## Modelo do módulo
`enxuto`: estende `tipografia` do `tokens.json` e a lista de fontes baixadas; teste de licença.

## Decisões do projeto aplicadas
ADR-0002 (fontes abertas, sem Pricedown), ADR-0001. Regras 4, 11.

## O que já existe
| Procurei | Onde | Achei | Decisão | Justificativa |
|---|---|---|---|---|
| Fontes e cache | `tipografia`, cache `~/.cache/costa-neon/fontes` | Bowlby One, Anton, Oswald, Josefin Sans | estender | Anton já existe; avaliar só se faltar peso ou corpo |

## Dependências novas
Possível fonte nova de fontsource (versão e licença conferidas, `SEG-07`); sem pacote de runtime.

## Rules e IDs da Constituição Aplicáveis
`SEG-07`, `DUP-04`, `TST-01`, `GOV-01`; ADR-0002.

## Critérios de Aceitação Executáveis
- `uv run pytest tests/test_fontes.py` sai 0: licença OFL ou Apache na API do fontsource, nome fora da lista bloqueada.
- `uv run costa_neon.py tokens build --checar` sai 0.
- Conferência visual (Regra 11): PNG de amostra do `titulo-letreiro` olhado pelo agente.
