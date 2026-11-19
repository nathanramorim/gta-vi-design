# Guia de ilustração — Costa Neon

O texto vem dos dados desta pasta; o comando `prompt` monta tudo. Não copie hex à mão: os do BLOCO DE ESTILO já são os tokens.

| Arquivo | O que tem |
|---|---|
| `estilo.txt` | BLOCO DE ESTILO (inglês), abre todo prompt de imagem |
| `receitas.json` | personagem por foto, personagem aleatório, cenário e imagem temática |
| `listas.json` | listas de sorteio; `PESSOA` varia gênero, origem e idade entre personagens |
| `tematica.json` | temas da imagem temática e a montagem de cada formato |
| `escrita.json` | regras de texto (modo 5) |

## Os 6 modos
| Modo | Comando | Sai |
|---|---|---|
| 1 Design system | `prompt --modo 1` | o que rodar para gerar o sistema |
| 2 Personagem por foto | `prompt --modo 2 --foto-autorizada` | prompt de imagem; só com autorização da pessoa, só adultos, sem figuras públicas |
| 3 Personagem aleatório | `prompt --modo 3 --semente 7` | prompt sorteado; a mesma semente dá o mesmo texto |
| 4 Cenário | `prompt --modo 4 --semente 7` | ambiente sem personagem principal |
| 5 Escrita | `prompt --modo 5 --tipo sinopse` | regras do texto em {IDIOMA} |
| 6 Imagem temática | `prompt --modo 6 --tema capa --descricao "..."` | prompt + montagem do formato |

## Fazer
- Uma tela, um destaque: só um item com degradê de acento por vez.
- Texto branco sobre escuro ou sobre painel translúcido.
- Imagem gerada sempre sem texto; texto e interface entram na montagem.
- Nomes de cidade, bairro, rádio e marca sempre inventados.

## Evitar
- Preto puro (use a tinta), sombra que não seja roxa ou azul, fundo de cor chapada (exceto as barras).
- Qualquer logo, nome, personagem, mapa, tela ou fonte de obra existente; o `prompt` recusa nomes conhecidos.
- Foto de pessoa sem autorização dela, de criança ou de figura pública.
