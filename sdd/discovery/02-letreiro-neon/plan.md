# Plano — 02 letreiro-neon

De baixo para cima; uma task por feature (limite 7 por onda).

| Onda | Task | Feature | Entrega | Depende de | Rules / IDs |
|------|------|---------|---------|------------|-------------|
| 1 | 02-01 | Paleta e contraste de letreiro | Cores (lima, degradê de céu, painel), exceção do contorno claro, `validar` e teste de contraste | 01-01 | `DUP-04`, `TST-01`, ADR-0001/0007 |
| 1 | 02-02 | Tipografia de letreiro | Display condensado pesado + sans de corpo (OFL), estilo `titulo-letreiro` com contorno e sombra | 02-01 | `SEG-07`, `GOV-01`, ADR-0002 |
| 2 | 02-03 | Fundos e cenários | Listas e receita "moldura de silhuetas", `prompt --cena letreiro`, termos bloqueados | 02-01 | `ARQ-06`, `TST-03`, ADR-0002 |
| 2 | 02-04 | Peça de letreiro | Componente `painel-letreiro`, peça 4:5 e 1:1, `tema carrossel` com as novas cores | 02-02, 02-03 | `TST-01`, `DUP-03`, ADR-0004/0005 |

02-02 e 02-03 podem correr em paralelo depois da 02-01.
