# feat-01-05-guia-e-prompt — Guia de ilustração e CLI prompt (6 modos, com semente)

Iniciativa: `sdd/discovery/01-costa-neon/`. Branch: `feat/01-costa-neon`. Feature 05 do plano.

## Objetivo
`plugins/costa-neon/skills/costa-neon/ilustracao/` com o BLOCO DE ESTILO (`estilo.txt`, hex dos tokens), receitas, listas de sorteio, montagem por formato e regras de escrita, como dados; `GUIA.md` curto com o que fazer e evitar. `prompt --modo 1..6` monta o texto: modo 1 orienta o design system; 2 exige `--foto-autorizada` (declaração da pessoa); 3 e 4 sorteiam com `--semente` (mesma semente, mesmo texto); 5 devolve o roteiro de escrita em {IDIOMA}; 6 monta a imagem temática e a montagem do formato. Variáveis validadas na borda; nome de obra existente sai 2.

## Modelo do módulo
`enxuto`: `scripts/cn/prompt.py` + dados em `ilustracao/`; reusa `entrada.py` e `termos.py` da 01-01.

## Decisões do projeto aplicadas
ADR-0002 (sem nome de obra, fotos com autorização, só adultos, sem figuras públicas, sem geração por IA no repositório), ADR-0007 (hex do bloco = tokens). Regras 3, 4, 5, 12, 15.

## O que já existe
| Procurei | Onde | Achei | Decisão | Justificativa |
|---|---|---|---|---|
| BLOCO DE ESTILO e receitas | `docs/prompt-diretor-de-arte.md` seções 6 a 8 | texto do Nathan | estender | vira dados; hex trocados pelos tokens (ADR-0007) |
| Validação e termos | `scripts/cn/entrada.py`, `termos.py` (01-01) | borda e hash | reusar | `DUP-03` |

## Dependências novas
Nenhuma.

## Rules e IDs da Constituição Aplicáveis
`ARQ-06`, `SEG-01`, `SEG-05`, `TST-01`, `TST-03`, `TST-04`, `DUP-03`; rules `sdd-seguranca.md`, `sdd-codigo-e-testes.md`.

## Critérios de Aceitação Executáveis
- `uv run pytest tests/test_prompt.py` sai 0: modos 2, 3, 4 e 6 começam pelo BLOCO DE ESTILO literal do `estilo.txt`; mesma semente dá o mesmo texto e sementes diferentes variam; modo 2 sem `--foto-autorizada` sai 2; variável com termo bloqueado ou caractere proibido sai 2; nenhum hex fora dos tokens no texto gerado.
- `uv run plugins/costa-neon/skills/costa-neon/scripts/costa_neon.py validar` sai 0.
