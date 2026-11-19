# Stack — costa-neon

## Dependências

| Camada | Escolha | Versão | Motivo |
|--------|---------|--------|--------|
| Runtime | Python via `uv` | >= 3.11 | ADR-0003; nunca pip |
| Render (proposta) | Playwright + Chrome do sistema | fixar na feature 04 | ADR-0004, mesmo caminho do carrossel-studio |
| Fontes | fontsource (OFL-1.1) | por fonte, no `tokens.json` | ADR-0002 |
| Requisitos | motor requisitos-para-ia | v0.1.0 (vendorizado, `skills.lock`) | ADR-0006 |
| Testes | pytest + ruff | grupo `dev` | `TST-01`, `COD-02` |
| DB | none | | arquivos |

Hoje (discovery) só existem o motor de requisitos e a documentação; nenhuma dependência de runtime ainda.

## Layout do projeto (proposto)
```
tokens/            costa-neon.tokens.json (fonte única) e costa-neon.css (gerado)
scripts/           costa_neon.py (CLI: tokens build, validar, render telas, prompt, tema) e o motor de requisitos
fundamentos/       página de amostras (HTML)
componentes/       biblioteca com estados normal, foco, ativo, desabilitado
telas/             8 telas de referência (HTML -> PNG 1920x1080)
ilustracao/        guia, BLOCO DE ESTILO, receitas e listas de sorteio (dados)
temas/             exports por consumidor (carrossel, vídeo, readme, forge-sdd)
plugins/costa-neon/  skill replicável (proposta)
docs/              prompt-diretor-de-arte.md, diagramas/, img/
```
