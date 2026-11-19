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

Os scripts usam só a biblioteca padrão; nenhuma dependência de runtime.

## Layout do projeto
```
plugins/costa-neon/skills/costa-neon/   motor (a skill do plugin funciona sozinha, ADR-0005)
  scripts/costa_neon.py                 CLI: tokens build, validar, tema, prompt
  scripts/cn/                           um módulo por responsabilidade (entrada, tokens, css, validar, termos, prompt, temas, logo)
  tokens/                               costa-neon.tokens.json (fonte única) e costa-neon.css (gerado)
  ilustracao/                           BLOCO DE ESTILO, receitas, listas, temática, escrita, GUIA.md
  dados/termos-bloqueados.txt           SHA-256 dos nomes de obras existentes
scripts/                                motor de requisitos v0.1.0 (vendorizado)
tests/                                  pytest (lista legível de termos e hex a evitar só aqui)
docs/                                   prompt literal, diagramas, banner
fundamentos/ componentes/ telas/        features 02, 03 e 04 (próximas ondas)
```
