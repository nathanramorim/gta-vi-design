# feat-01-06-temas-e-plugin — Temas por consumidor e plugin costa-neon

Iniciativa: `sdd/discovery/01-costa-neon/`. Branch: `feat/01-costa-neon`. Feature 06 do plano.

## Objetivo
`tema carrossel|video|readme|forge-sdd|todos --saida <pasta> [--previa]`: gera `marca.json` + `marca/logo.svg` (carrossel), `.video-marca.json` (gerador-videos), `identidade.json` + `logo.svg.frag` (readme-studio), `forge-sdd-missoes.json` + `logo.svg` (Forge SDD "Edição Missões": 5 estações como missões), e `previa-<consumidor>.svg` para conferência visual. Escreve só em `--saida`; `--validar` não grava. Plugin em `plugins/costa-neon/` + marketplace na raiz, skill que só chama os scripts. O próprio banner do README passa a usar `tema readme`.

## Modelo do módulo
`enxuto`: `scripts/cn/temas.py` e `scripts/cn/logo.py`, sem estado.

## Decisões do projeto aplicadas
ADR-0005 (um tema por consumidor, plugin), ADR-0001 (gerado dos tokens), ADR-0002 (logo próprio: sol listrado), ADR-0003. Regras 3, 11, 12, 15.

## O que já existe
| Procurei | Onde | Achei | Decisão | Justificativa |
|---|---|---|---|---|
| Arquivo de marca | carrossel-studio `sdd/spec/contrato-carrossel.md`, `marca.py` | `cores` bg/surface/text/muted/accent/accent2/danger, `fontes` title/body/mono, `logo` | estender (export) | o consumidor não muda |
| Marca do vídeo | gerador-videos `motor/marca/papeis.py`, `override.py` | mesmos papéis + `success` | estender | idem |
| Identidade do banner | readme-studio `exemplos/forge-sdd/identidade.json` | chaves do banner | estender | idem |
| Estações | forge-sdd `site/src/data/stations.ts` | 5 estações | estender | só nomes das estações; nada copiado |
| Plugin | carrossel-studio `.claude-plugin/marketplace.json` | marketplace na raiz | reusar o padrão | instalação igual |

## Dependências novas
Nenhuma.

## Rules e IDs da Constituição Aplicáveis
`ARQ-03`, `ARQ-05`, `ARQ-06`, `SEG-01`, `SEG-02`, `TST-02`, `DUP-03`; rules `sdd-arquitetura.md`, `sdd-seguranca.md`.

## Critérios de Aceitação Executáveis
- `uv run pytest tests/test_temas.py` sai 0: chaves e cores de cada tema batem com os tokens; o tema do carrossel passa no `carregar_marca` do carrossel-studio quando ele existir na máquina (senão o teste é pulado e diz por quê); `--validar` não grava; caminho de saída inválido sai 2.
- As prévias (`--previa`) são renderizadas e olhadas antes da entrega.
- `uv run plugins/costa-neon/skills/costa-neon/scripts/costa_neon.py validar` sai 0; `verificar_readme.py README.md` sai 0.
