# Discovery 01 — Costa Neon, design system replicável

Fonte de verdade: [`docs/prompt-diretor-de-arte.md`](../../../docs/prompt-diretor-de-arte.md) (texto do Nathan, guardado sem alteração). Onde esta discovery ou uma ADR diverge do prompt, vale a decisão registrada aqui (ex.: fonte display Bowlby One, ADR-0002).

## Problema
O Nathan tem um prompt de diretor de arte muito detalhado (cores exatas, tipografia, telas, componentes, receitas de imagem), mas ele só existe como texto. Cada vez que uma ferramenta (carrossel, vídeo, banner de README, lançamento do Forge SDD) quer esse visual, alguém precisa reinterpretar o texto e copiar hex à mão. O resultado varia e pode escorregar para cópia de marca existente.

## Para quem
- **Nathan e as ferramentas dele** (carrossel-studio, gerador-videos, readme-studio, Forge SDD, marketing do hub): querem um tema pronto, igual em todo lugar.
- **Qualquer pessoa que instale o design system** e troque `{SISTEMA}`, `{MARCA}`, `{CIDADE}`, `{IDIOMA}` e `{FORMATO}` para ter o seu.
- **Uma IA** que precisa gerar tela ou prompt de imagem sem inventar valores: ela chama scripts, não chuta hex.

## Jornada (exemplo simples)
1. A pessoa instala o plugin `costa-neon` e define `{MARCA} = Acme`, `{CIDADE} = Palmarena` (nomes fictícios).
2. Pede à IA "faz um post 1:1 de lançamento". A IA roda `prompt --modo 6 --formato 1:1` e recebe o prompt de imagem em inglês, começando pelo BLOCO DE ESTILO, sem nenhum nome de obra existente.
3. Pede "me dá o tema para o carrossel". A IA roda `tema carrossel --saida .` e o carrossel-studio já usa as cores e fontes.
4. Antes de entregar uma tela, a IA roda `validar` e olha o PNG.

## O que o repositório entrega (seção 9 do prompt)
| # | Entrega | Como fica no repositório |
|---|---------|--------------------------|
| 1 | Tokens em JSON e CSS (cores, degradês, tipografia, espaçamento, raios, sombras) | `tokens/costa-neon.tokens.json` (fonte única) e `tokens/costa-neon.css` gerado por `tokens build` |
| 2 | Página de fundamentos com amostras | `fundamentos/index.html` gerada dos tokens + PNG de conferência |
| 3 | Componentes com estados normal, foco, ativo, desabilitado | `componentes/` (aba, chip de gatilho, ícone de botão, seletor, cabeçalho, navegação, lista, painel de descrição, radar, vida/energia, alerta/dinheiro, item equipado, atalhos, menu de pausa, roda de seleção, roda de rádio, caixa de ajuda) |
| 4 | As 8 telas de referência em 1920x1080 | `telas/01-loading` … `telas/08-encerramento` (HTML) e `render telas` -> PNG |
| 5 | Guia de ilustração com BLOCO DE ESTILO e receitas | `ilustracao/` (bloco, 4 receitas e listas de sorteio como dados) + `prompt` (6 modos) |
| 6 | Lista do que fazer e do que evitar | `docs/fazer-e-evitar.md`, com as regras do prompt e as desta discovery |

## Como outras ferramentas consomem (um "tema" por consumidor)
| Consumidor | O que já lê hoje | Export proposto |
|------------|------------------|-----------------|
| carrossel-studio | arquivo de marca JSON (`cores` bg/surface/text/muted/accent/accent2/danger, `fontes` title/body/mono do fontsource, `logo`) | `tema carrossel` -> `costa-neon.marca.json` (passa no `--validar` do carrossel) |
| gerador-videos | `conteudo/.video-marca.json` (override), tokens, `identidade.json` | `tema video` -> `.video-marca.json` |
| readme-studio | `docs/img/identidade.json` (fundo, brilho, texto, suave, acento[3], painel, borda, fontes, logo) | `tema readme` -> `identidade.json` + `logo.svg.frag` (este README já usa) |
| **Forge SDD "Edição Missões"** (primeiro consumidor) | discovery 101 aprovada no forge-sdd (PR #111, rascunho): banner do README, notas da 5.0.0, posts; estações como "missões" | `tema forge-sdd` -> cores das 5 missões (Concepção, Planejamento, Construção, Governança, Operação) dentro da lista de hex, letreiro próprio, mascotes do site redesenhados no estilo (contorno `#201C24`, luz de pôr do sol) |
| Marketing do hub (reel/carrossel "Minhas missões") | via carrossel-studio e gerador-videos | mesmos temas acima |

## Vira plugin/skill?
Sim, proposta (ADR-0005): plugin `costa-neon` em `plugins/costa-neon/` com uma skill replicável. A skill não desenha nada sozinha: ela chama scripts determinísticos como ferramentas.

| Script | O que faz |
|--------|-----------|
| `tokens build` | gera o CSS a partir do `tokens.json` |
| `validar` | reprova hex fora da lista do prompt (62 valores, incluindo `#A6699D`, `#A06282`, `#D07178`, `#181818` das seções 2 e 4, mais a sombra `rgba(40,10,40,0.45)`), sombra que não seja roxa ou azul, contorno que não seja ameixa (`#201C24`), tela sem as barras `#171717` de 9% e sem a linha neon, e "Pricedown" ou nome de obra existente só nos artefatos distribuídos (`tokens/`, `fundamentos/`, `componentes/`, `telas/`, `ilustracao/`, `temas/`, `plugins/`, `README.md`), nunca em `sdd/` nem no `docs/prompt-diretor-de-arte.md` |
| `render telas` | HTML -> PNG 1920x1080 + folha de contato para a conferência visual |
| `prompt` | monta o prompt de imagem: BLOCO DE ESTILO + receita + variáveis, nos 6 modos; sorteio com `--semente` (mesmo resultado sempre); recusa nome de obra existente nas variáveis |
| `tema <consumidor>` | gera o arquivo de cada consumidor |

## Regras de negócio
1. Uma tela, um destaque: só um item com gradiente de acento por vez.
2. Texto sempre legível: branco sobre escuro ou sobre painel translúcido.
3. Ilustração nunca usa preto puro; sombra sempre roxa ou azul; fundo sempre degradê, exceto as barras.
4. "Contorno preto" do prompt (texto display, ícones do mapa) vira a tinta `#201C24` (proposta, Gate 1), para cumprir "contorno ameixa" da regra 5 do prompt.
5. Imagem gerada sempre sem texto; texto e interface entram na montagem.

## Originalidade e propriedade intelectual (decisões)
Explicando simples: dá para lembrar o "clima" de um gênero (pôr do sol, neon, palmeiras), mas não dá para copiar o que é marca ou obra de alguém (logo, letreiro, fonte do letreiro, personagem, mapa, tela de um jogo).

| Tema | Decisão |
|------|---------|
| Fonte display | **Bowlby One (aberta) é o padrão.** Pricedown fica fora dos padrões, das pilhas de fallback e dos exemplos (é fortemente associada ao logotipo de uma série de jogos existente). ADR-0002 |
| HUD (radar, estrelas de alerta, dinheiro, roda de itens, roda de rádio) | São convenções do gênero. Fazemos com layout, ícones e proporções nossos e com a paleta do repositório; nunca replicar o layout ou os ícones exatos de um jogo existente |
| Nomes | Cidade, bairros, rádios, artistas e marcas sempre inventados; `validar` e `prompt` recusam uma lista de nomes de obras existentes (a lista fica só nos testes) |
| Geração de imagem | Só com prompts sem nome de obra, marca, personagem ou local existente; o AVOID do BLOCO DE ESTILO já pede isso |
| Fotos de pessoas | Só com autorização da pessoa, só adultos, sem figuras públicas; a autorização é declaração da pessoa, nunca do agente |
| Paleta | Ver risco R1: os hex do prompt quase coincidem com um conceito de fã publicado com direitos reservados. Cor sozinha tem risco baixo; as telas serão composição nossa. Pergunta no Gate 1 |

## Fontes e licenças
Licenças conferidas na API do fontsource (`api.fontsource.org/v1/fonts/<id>`) em 2026-11-19.

| Papel | Fonte | Licença | Pesos disponíveis |
|-------|-------|---------|-------------------|
| Display (menu, abas, dinheiro) | **Bowlby One** | OFL-1.1 | 400 |
| Texto e títulos de tela | Josefin Sans (alternativa: Outfit) | OFL-1.1 / OFL-1.1 | 100–700 / 100–900 |
| Rótulo de seção (script) | Kaushan Script | OFL-1.1 | 400 |
| Título de prancha (slab) | Zilla Slab | OFL-1.1 | 300–700 |
| Título gigante | Anton | OFL-1.1 | 400 |
| Rodas e HUD | Oswald | OFL-1.1 | 200–700 |

Como chegam: baixadas do fontsource (jsDelivr) uma vez para `~/.cache/costa-neon/fontes` (ou `COSTA_NEON_CACHE`) e embutidas no HTML na hora do render, como no carrossel-studio. Os arquivos de fonte **não** entram no git. Os temas exportados citam o nome da fonte; quem consome baixa pelo mesmo caminho. Bowlby One só tem peso 400: o "peso" vem do desenho da fonte e do contorno de 2 a 3px.

## Escopo
**Dentro:** as 6 entregas da seção 9; scripts `tokens build`, `validar`, `render telas`, `prompt`, `tema`; plugin/skill; exports para carrossel-studio, gerador-videos, readme-studio e Forge SDD; README e diagramas; CI em macOS, Linux e Windows.
**Fora (nesta iniciativa):** gerar imagens com IA dentro do repositório (o `prompt` devolve o texto; a geração é com a pessoa); site publicado na web; fontes pagas; aplicar o tema nos repositórios consumidores (cada um faz por `/nova-feature` lá).

## Riscos
| # | Risco | Mitigação |
|---|-------|-----------|
| R1 | **Paleta e lista de telas quase iguais a um conceito de fã** ("UI Concept" publicado no Behance em 2025, direitos reservados ao autor). A branch `feat/readme-v5-gta-vi` do forge-sdd mediu esses valores: `#E28643`/`#e28642`, `#FE7594`/`#fe7694`, `#6A1A3C`/`#6b193c`, `#BF52DB`/`#be50db`, `#434967`/`#434a68`. As 8 telas espelham as pranchas daquele conceito | Cores sozinhas: risco baixo. Telas desenhadas do zero, com composição nossa; nenhuma arte, captura ou arquivo do conceito entra aqui. Gate 1: creditar como inspiração? |
| R2 | Escorregar para cópia de marca (letreiro, ícones de HUD, nomes) | ADR-0002, regra 4, `validar` com termos proibidos, revisão de PI por peça |
| R3 | Material do forge-sdd em conflito com a própria decisão 101: a branch `feat/readme-v5-gta-vi` tem "Design system GTA VI" no caminho e no README, pilhas com Pricedown e uma fonte com o nome do jogo | Não copiar os `tokens.*` dela; propor no Gate 1 que o Costa Neon substitua esse material como tema da "Edição Missões" |
| R4 | Ilustrações das telas (loading, céu, encerramento) exigem arte | v0.1 com formas vetoriais próprias (sol listrado, palmeiras, ondas, flamingos em silhueta); ilustração pintada fica para depois, via `prompt` |
| R5 | Render depende de Chrome; diferenças entre sistemas | Playwright com Chrome do sistema e fallback Chromium (como o carrossel-studio); CI nos 3 sistemas |
| R6 | Formato dos consumidores muda | Testes de contrato por tema (ex.: tema do carrossel passa no `--validar` dele) |

## Material complementar lido (somente leitura)
- forge-sdd, PR #111 (rascunho), `sdd/discovery/101-tema-missoes-v5/`: homenagem ao clima, sem letreiro, logo, "VI", personagens ou interface; estações como "missões"; aplicar primeiro em banner do README, notas da 5.0.0 e posts.
- forge-sdd, branch `feat/readme-v5-gta-vi` (sem PR): ver R1 e R3.
- forge-sdd, `site/src/data/stations.ts` e `MascotFallbackSvg.astro`: 5 estações com cor e marca (anel, losango, barra, onda, triângulo) e mascotes próprios. Personagens originais do Forge SDD, candidatos a aparecer redesenhados no estilo Costa Neon.

## Perguntas para o Nathan (Gate 1)
1. **Nome e visibilidade:** `nathanramorim/costa-neon`, privado. Confirma? Fica público depois?
2. **Fonte display:** Bowlby One como padrão e Pricedown fora de tudo (padrões, fallback e exemplos). Aprova?
3. **Paleta (R1):** manter os hex do prompt (cor não é marca; telas serão composição nossa) e citar o conceito do Behance como inspiração no README? Ou ajustar a paleta para se afastar mais?
4. **Contorno:** o "contorno preto" do prompt vira `#201C24` (tinta ameixa)? Barras continuam `#171717` e a lateral do menu de pausa `#181818`?
5. **Forge SDD "Edição Missões" (forge-sdd PR #111):** aplicar o Costa Neon como tema dela, no lugar da branch `feat/readme-v5-gta-vi`? E no marketing do hub (reel e carrossel "Minhas missões")?
6. **Padrões de exemplo:** `{MARCA} = Acme` e `{CIDADE} = Palmarena` (fictícios) servem? Prefere outros nomes?
7. **Arquitetura proposta:** render HTML -> PNG no Chrome local (ADR-0004) e plugin/skill `costa-neon` com temas por consumidor (ADR-0005). Aprova?
8. **Ilustração na v0.1:** formas vetoriais próprias nas telas (recomendado) ou já usar imagens geradas por IA a partir do `prompt`? Se IA, qual gerador?
9. **Ordem:** tudo (features 01 a 07) ou primeiro o mínimo útil (01 tokens, 05 prompt, 06 temas) para atender a Edição Missões rápido?
10. **Licença do repositório:** ainda não há `LICENSE`. MIT como no carrossel-studio, outra, ou nenhuma enquanto for privado?

## Dono
Nathan (produto e direção de arte). Construção pelo fluxo Forge SDD.

## Decisões do Gate 1 (Nathan, 19/11/2026: "recomendações")
1. Nome `costa-neon`; privado por enquanto, público depois da v0.1.
2. Bowlby One é o display padrão; Pricedown fora de tudo (ADR-0002).
3. Paleta: cada hex deslocado um pouco, mesmo visual, nenhum valor a ±3 por canal do conceito; o prompt fica literal; `tokens.json` + ADR-0007 (tabela origem → token) são a fonte do hex final; o `validar` usa os tokens.
4. "Contorno preto" vira a tinta ameixa deslocada (`cor.tinta`).
5. Costa Neon é o tema do Forge SDD "Edição Missões" (no lugar da branch `feat/readme-v5-gta-vi`) e do marketing do hub. Registrado como decisão e consumidor; aplicar lá é fix separado, sem mexer no forge-sdd nem no hub agora.
6. Exemplos: `{MARCA}=Acme`, `{CIDADE}=Palmarena`.
7. ADR-0004 e ADR-0005 aprovadas.
8. Ilustrações da v0.1: formas vetoriais próprias, sem geração por IA.
9. Primeiro o mínimo: features 01 (tokens + validador), 05 (guia + `prompt`, 6 modos, com semente) e 06 (temas + plugin). 02, 03, 04 e 07 ficam para as próximas ondas.
10. Licença MIT (LICENSE e README atualizados).
