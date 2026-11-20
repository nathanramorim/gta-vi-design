# feat-02-03-fundos-e-cenarios — Fundos e cenários para imagem

Iniciativa: `sdd/discovery/02-letreiro-neon/`. Branch: `feat/02-letreiro-neon`. Task 02-03 do plano.

## Objetivo
Listas de sorteio em `ilustracao/` (moldura de silhuetas: palmeira, skyline, ponte sobre a água, carro em primeiro plano, helicóptero; céu de pôr do sol por degradê do token) e receita `letreiro`. `prompt --cena letreiro --semente N` monta o prompt do fundo: sem texto na imagem, miolo livre para o título, placas e logos inventados e ilegíveis, hex dos tokens. Termos bloqueados estendidos.

## Modelo do módulo
`enxuto`: estende `ilustracao/*.json`, `scripts/cn/prompt.py` e `dados/termos-bloqueados.txt`.

## Decisões do projeto aplicadas
ADR-0002 (prompts sem nome de obra), ADR-0007 (hex dos tokens). Regras 4, 12.

## O que já existe
| Procurei | Onde | Achei | Decisão | Justificativa |
|---|---|---|---|---|
| Motor com semente | `prompt.py` (01-05) | 6 modos, `--semente` | estender | mesma montagem |
| Listas | `ilustracao/listas.json`, `tematica.json` | listas de sorteio | estender | `DUP-01` |

## Dependências novas
Nenhuma.

## Rules e IDs da Constituição Aplicáveis
`ARQ-06`, `SEG-01`, `TST-03`, `DUP-03`; ADR-0002.

## Critérios de Aceitação Executáveis
- `uv run pytest tests/test_prompt.py tests/test_listas.py` sai 0: mesma semente, mesmo texto; sem termo bloqueado; sem pedir texto na imagem; listas com todos os elementos e nenhuma marca; nenhum hex fora dos tokens.
- `uv run costa_neon.py validar` sai 0.
