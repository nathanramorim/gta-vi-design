# Plano — 01 costa-neon

De baixo para cima: primeiro a fonte única (tokens), depois o que lê dela. Cada feature vira tasks no `/split-features` (até 7 por onda), depois do Gate 1.

| Onda | Feature | Entrega | Depende de | Paralelo com | Rules / IDs |
|------|---------|---------|------------|--------------|-------------|
| 1 | 01 tokens + validador | `tokens.json`, `tokens build`, `validar`, CI 3 sistemas | — | — | `DUP-04`, `TST-01`, `SEG-01`, ADR-0001/0002/0003 |
| 1 | 05 guia de ilustração + `prompt` | BLOCO DE ESTILO, receitas, listas, 6 modos, `--semente` | 01 | 02 | `ARQ-06`, `SEG-01`, ADR-0002 |
| 1 | 02 fundamentos | página de amostras + PNG | 01 | 05 | `ARQ-03`, regra 11 |
| 2 | 03 componentes | 17 componentes x 4 estados | 01, 02 | 06 | `DUP-03`, `TST-01` |
| 2 | 06 exports para consumidores | `tema carrossel|video|readme|forge-sdd` + plugin/skill | 01 | 03 | `ARQ-06`, `TST-02`, ADR-0005 |
| 3 | 04 telas 1–8 | HTML + `render telas` 1920x1080 + folha | 03 | — | `TST-01`, ADR-0004 |
| 3 | 07 README e site | README com telas reais, `docs/fazer-e-evitar.md`, diagramas | 04, 06 | — | `FLX-07`, ADR-0006 |

Caminho curto para a "Edição Missões" do Forge SDD (se o Nathan escolher no Gate 1): 01 -> 05 -> 06.
