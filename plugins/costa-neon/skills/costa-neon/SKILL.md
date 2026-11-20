---
name: costa-neon
description: Design system Costa Neon (pôr do sol tropical, neon, art déco). Use quando pedirem cores, tokens, CSS, tema para carrossel, vídeo, banner de README ou Forge SDD, prompt de imagem nesse estilo (personagem, cenário, capa, post, story), textos de tela, ou para conferir se uma peça segue o Costa Neon. Nunca invente cor: rode os scripts.
---

# Costa Neon

Design system replicável. Você **não escreve hex nem CSS à mão**: chama o script, que lê o `tokens.json` e responde sempre igual.

`CN="${CLAUDE_PLUGIN_ROOT}/skills/costa-neon/scripts/costa_neon.py"` (fora do plugin: o caminho desta pasta + `scripts/costa_neon.py`). Rode com `uv run "$CN" ...`. Nunca use pip.

## O que pedir ao script
| Pedido | Comando |
|---|---|
| CSS dos tokens | `uv run "$CN" tokens build` (o arquivo fica em `tokens/costa-neon.css`) |
| Conferir uma peça ou pasta | `uv run "$CN" validar <caminho>`; código 2 lista o que está fora |
| Tema de uma ferramenta | `uv run "$CN" tema carrossel|video|readme|forge-sdd|todos --saida <pasta> --previa` |
| Prompt de imagem ou texto | `uv run "$CN" prompt --modo 1..6 [--semente N] [--formato 16:9|1:1|9:16]` |

Modos do `prompt`: 1 design system, 2 personagem por foto (só com `--foto-autorizada`), 3 personagem aleatório, 4 cenário, 5 escrita (`--tipo`), 6 imagem temática (`--tema`, `--descricao`). `prompt --cena letreiro --semente N` monta o fundo de peça (moldura de silhuetas, sem texto na imagem). Detalhes em `ilustracao/GUIA.md`.

## Como trabalhar
1. Pegue `{MARCA}`, `{CIDADE}`, `{IDIOMA}` e `{FORMATO}` da pessoa; sem resposta, use os padrões do `tokens.json` (nomes fictícios).
2. Rode o comando. Com `--previa`, abra o `previa-<consumidor>.svg` (ou um PNG dele) e **olhe** antes de entregar.
3. Antes de entregar qualquer peça, rode `validar` nela.
4. Para imagem: entregue o prompt que o script devolveu, sem editar o BLOCO DE ESTILO. A imagem sai sem texto; texto e interface entram na montagem.

## Regras
- Tudo original: nenhum logo, nome, personagem, mapa, tela ou fonte de obra existente. Nomes de cidade, bairro, rádio e marca sempre inventados. O script recusa nomes conhecidos (código 2).
- Foto de pessoa só com autorização dela, só adultos, sem figuras públicas. `--foto-autorizada` é a declaração da pessoa; nunca marque por ela.
- Fontes abertas: display Bowlby One; texto Josefin Sans; script Kaushan Script; slab Zilla Slab; gigante Anton; HUD Oswald.
- No arquivo de marca (carrossel e vídeo), o título é Oswald porque o carrossel pede pesos 400 a 600.
- Tema `video`: passe a raiz do projeto em `--saida`; ele grava `conteudo/.video-marca.json` e `conteudo/marca/logo.svg`.
- `tema` sobrescreve os arquivos do tema na `--saida`.
