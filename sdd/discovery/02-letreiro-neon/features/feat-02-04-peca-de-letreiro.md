# feat-02-04-peca-de-letreiro — Peça de letreiro (cartaz e post)

Iniciativa: `sdd/discovery/02-letreiro-neon/`. Branch: `feat/02-letreiro-neon`. Task 02-04 do plano.

## Objetivo
Componente `painel-letreiro` (fundo escuro, contorno claro, cantos chanfrados), faixa de chamada rosa e chips lima; peça HTML -> PNG em 4:5 (1080x1350) e 1:1 (1080x1080) com título, 2 painéis, faixa de chamada e rodapé sobre um fundo gerado. `tema carrossel` e `tema forge-sdd` ganham as cores e fontes de letreiro.

## Modelo do módulo
`enxuto`: estende `componentes/`, render (ADR-0004) e `temas`; sem módulo novo.

## Decisões do projeto aplicadas
ADR-0004 (Chrome local), ADR-0005 (temas), ADR-0002 (peça original, nada copiado da referência). Regras 4, 8, 11.

## O que já existe
| Procurei | Onde | Achei | Decisão | Justificativa |
|---|---|---|---|---|
| Render HTML -> PNG | ADR-0004, carrossel-studio | Chrome local | reusar | já decidido |
| Temas | `tema carrossel`, `tema forge-sdd` (01-06) | export dos tokens | estender | só novas chaves |

## Dependências novas
Playwright e Pillow só se a 01 ainda não os fixou (consultar a documentação na versão exata, `SEG-07`).

## Rules e IDs da Constituição Aplicáveis
`TST-01`, `DUP-03`, `SEG-07`, `ARQ-06`; ADR-0004, ADR-0005.

## Critérios de Aceitação Executáveis
- `uv run pytest tests/test_peca.py` sai 0: 4:5 = 1080x1350, 1:1 = 1080x1080, com título, 2 painéis, faixa de chamada e rodapé; contraste >= 4,5:1.
- `uv run costa_neon.py tema carrossel --saida <dir>` passa no `--validar` do carrossel-studio.
- `uv run costa_neon.py validar` e `uv run ruff check` saem 0.
- Conferência visual (Regra 11): agente olha o PNG ao lado da referência; sem cópia de layout, texto ou arte.
