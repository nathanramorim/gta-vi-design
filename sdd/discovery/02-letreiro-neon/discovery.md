# Discovery 02 — Letreiro Neon: paleta, fonte, fundos e cenários para peças de imagem

Depende da 01 (tokens, `validar`, `prompt`, temas). Branch `feat/02-letreiro-neon`, partindo de `feat/01-costa-neon` para herdar os tokens.

## Clarify (respostas do Nathan, 20/11/2026)
| Sinal | Pergunta | Resposta |
|-------|----------|----------|
| Escopo com 2 leituras | "Temática completa do GTA VI" copia a obra ou se inspira? | **Estética inspirada, sem marca.** Regra 4 e ADR-0002 ficam como estão: nada de nome GTA, Pricedown, arte ou logo da obra. Absorvemos paleta, contraste, fundos, cenários e peso da tipografia, tudo original. |
| Dependência | Nova iniciativa ou dentro da 01? | **Nova iniciativa 02**, pois a 01 está no PR #1 aguardando a Camada C. |
| Critério ausente | O que a referência altera? | **Os quatro:** paleta e contraste, tipografia de letreiro, fundos e cenários, peça de letreiro (cartaz/post). |

## Problema
A 01 entrega tokens e prompts voltados a telas de HUD em 1920x1080. A referência do Nathan (post de Instagram 4:5, "nova missão desbloqueada") mostra outro uso: **letreiro e peça de marketing**. Faltam a paleta de céu em degradê com acento lima, o painel escuro com contorno claro, o título branco e rosa com contorno grosso e a cena de fundo (palmeiras, skyline, ponte, carro, helicóptero). Hoje cada peça reinventaria isso, e a IA de imagem escorregaria para a obra de origem.

## Para quem
Nathan e as ferramentas dele (carrossel-studio, gerador-videos, readme-studio, Forge SDD "Edição Missões", marketing do hub), e qualquer pessoa que instale o plugin e troque `{MARCA}`, `{CIDADE}`.

## O que a referência ensina (leitura de design, sem copiar a peça)
| Dimensão | Observação | Vira |
|----------|------------|------|
| Céu | Degradê vertical roxo, magenta, laranja, amarelo no horizonte | Degradê `ceu-letreiro` nos tokens (hex deslocados, ADR-0007) |
| Acento | Verde-lima vivo sobre painel escuro: o único tom frio quente-contra-quente | Cor `lima-destaque` + regra de uso (um por peça, só em valor/oferta) |
| Painéis | Fundo quase preto, contorno claro (creme/laranja) e cantos chanfrados | Componente `painel-letreiro`; contorno claro permitido só aqui |
| Título | Letras brancas e rosa-choque, contorno escuro grosso e sombra dura, levemente inclinadas | Estilo `titulo-letreiro` (contorno `cor.tinta`, sombra roxa) |
| Texto | Corpo em sans limpa e legível sobre o painel; números em negrito | Par de fontes: display de letreiro + sans de corpo |
| Fundo | Silhuetas escuras nas bordas (palmeira, prédio, carro) emoldurando o miolo claro | Receita de cenário "moldura de silhuetas" |
| Cenário | Pôr do sol, skyline, ponte sobre a água, carro em primeiro plano, helicóptero | Listas de sorteio de cenário em `ilustracao/` |
| Contraste | Texto claro sobre painel escuro; texto escuro sobre faixa rosa e lima | Critério numérico (WCAG 4,5:1 texto, 3:1 título) |

## Regras de negócio
1. Nenhum valor fora do `tokens.json`; toda cor nova entra com hex deslocado (ADR-0007) e a `validar` passa a conhecê-la.
2. Contorno de texto e de forma continua `cor.tinta` (Regra 8); contorno claro só no `painel-letreiro`, como exceção declarada no token.
3. Prompts de imagem nunca citam obra existente nem pedem "estilo de jogo"; descrevem cena, luz e paleta.
4. Placas, logos, placas de carro e letreiros dentro da cena são inventados e ilegíveis por padrão.
5. Texto da peça vai por HTML (nunca desenhado pela IA de imagem), para ficar exato e passar no contraste.

## Escopo
**Dentro:** 4 features (02-01 a 02-04), tokens, `validar`, `prompt`, tema do carrossel, componente e peça 4:5 e 1:1 em PNG.
**Fora:** telas HUD da 01 (ondas 2 e 3 dela seguem), vídeo, qualquer fonte ou arte da obra, personagens.

## Riscos
| # | Risco | Mitigação |
|---|-------|-----------|
| R1 | Paleta e composição ficarem iguais à peça de referência | Hex deslocados, cena sorteada por semente, `validar` e Camada B conferem; comparar lado a lado |
| R2 | Lima + rosa + laranja reprovarem no contraste | Critério numérico executável por par de cores |
| R3 | Fonte condensada pesada com licença incerta | Só OFL/Apache conferida na API do fontsource antes de entrar (Regra 11); Pricedown e similares barradas |
| R4 | A IA de imagem trazer logos ou texto da obra | AVOID no BLOCO DE ESTILO e lista de termos bloqueados estendida |
| R5 | O pedido original ("temática completa do GTA VI") conflitar com a Regra 4 | Decidido no clarify; se o Nathan mudar de ideia, `/constitution` antes de continuar |
