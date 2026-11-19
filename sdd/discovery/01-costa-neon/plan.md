# Plano — 01 costa-neon

Revisado no Gate 1 (resposta 9): primeiro o mínimo útil para a "Edição Missões". De baixo para cima; uma task por feature.

| Onda | Task | Feature | Entrega | Depende de | Rules / IDs |
|------|------|---------|---------|------------|-------------|
| 1 | 01-01 | 01 tokens + validador | `tokens.json` (paleta deslocada), `tokens build`, `validar`, CI 3 sistemas | — | `DUP-04`, `TST-01`, `SEG-01`, `COD-02`, ADR-0001/0002/0003/0007 |
| 1 | 01-05 | 05 guia de ilustração + `prompt` | BLOCO DE ESTILO com os hex dos tokens, receitas, listas, 6 modos, `--semente` | 01-01 | `ARQ-06`, `SEG-01`, `TST-03`, ADR-0002 |
| 1 | 01-06 | 06 temas + plugin | `tema carrossel|video|readme|forge-sdd`, prévia SVG, plugin `costa-neon` | 01-01 | `ARQ-06`, `TST-02`, `DUP-03`, ADR-0005 |
| 2 | — | 02 fundamentos | página de amostras + PNG | 01-01 | `ARQ-03`, regra 11 |
| 2 | — | 03 componentes | 17 componentes x 4 estados | 02 | `DUP-03`, `TST-01` |
| 3 | — | 04 telas 1–8 | HTML + `render telas` 1920x1080 + folha | 03 | `TST-01`, ADR-0004 |
| 3 | — | 07 README e site | README com telas reais, `docs/fazer-e-evitar.md` | 04, 06 | `FLX-07`, ADR-0006 |

01-05 e 01-06 podem correr em paralelo depois de 01-01.
