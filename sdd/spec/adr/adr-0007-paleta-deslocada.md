# ADR-0007: Paleta deslocada — tokens.json é a fonte do hex final

- **Data:** 2026-11-19
- **Status:** `aprovado` (Gate 1, resposta 3)
- **Regras afetadas (IDs da constitution):** Regras 4 e 8, `DUP-04`, `GOV-01`
- **Autor / Responsável:** dono do repositório

## Contexto
Os hex do prompt (`docs/prompt-diretor-de-arte.md`) quase coincidem, canal a canal, com valores medidos de um conceito de interface de terceiros publicado com todos os direitos reservados (risco R1 da discovery 01). O Nathan decidiu no Gate 1 manter o visual e afastar cada cor.

## Opções Consideradas
1. **Manter os hex do prompt:** fiel ao texto, mas igual ao conceito.
2. **Deslocar cada hex um pouco, de forma consistente, e manter o prompt literal como fonte de intenção:** mesmo clima, valores próprios.

## Decisão
Opção 2. Regra do deslocamento (feita uma vez, valores congelados no `tokens.json`):
- Cores com saturação: matiz +5° (HLS), mantendo luz e saturação; se ainda ficasse perto, a menor variação de matiz, luz ou saturação que resolvesse.
- Neutros (cinzas, pretos e branco): uma tinta ameixa leve (matiz 320°).
- Aceite: cada hex final fica a **4 ou mais pontos em algum canal** (fora de ±3) de **todo** valor do conceito e de **todo** hex original do prompt, e a 4 ou mais de qualquer outro token. O teste `tests/test_paleta.py` confere com `tests/dados/evitar-hex.txt`.
- "Contorno preto" do prompt vira `cor.tinta` (resposta 4 do Gate 1).
- O `validar` usa os hex do `tokens.json` como lista permitida; o prompt continua literal e fora da validação.

## Mapa origem → token
| Origem (prompt) | Token | Valor final |
|---|---|---|
| `#FEA96B` | `degrade.sunset[0]` | `#FEB56B` |
| `#FF8788` | `degrade.sunset[1]` | `#FF9087` |
| `#FA7796` | `degrade.sunset[2]` | `#FA778B` |
| `#C06397` | `degrade.sunset[3]` | `#C0638F` |
| `#A56F9E` | `degrade.sunset[4]` | `#A56F9A` |
| `#FDAA6C` | `degrade.acento[0]` | `#FDBB6C` |
| `#FE7693` | `degrade.acento[1]` | `#FE7688` |
| `#E851AB` | `degrade.acento[2]` | `#E8519E` |
| `#FBA373` | `degrade.neon[0]` | `#FBAE73` |
| `#FF8492` | `degrade.neon[1]` | `#FF8484` |
| `#EF60AE` | `degrade.neon[2]` | `#EF60A2` |
| `#34489C` | `degrade.ceu[0]` | `#343F9C` |
| `#4A50B9` | `degrade.ceu[1]`, `degrade.sol[0]` | `#4D4AB9` |
| `#7F5DA1` | `degrade.ceu[2]` | `#885DA1` |
| `#CA85A7` | `degrade.ceu[3]` | `#CA85A1` |
| `#FEAF6E` | `degrade.ceu[4]` | `#FEC06E` |
| `#894CC7` | `degrade.sol[1]` | `#934CC7` |
| `#E448C7` | `degrade.sol[2]` | `#E448BA` |
| `#F268A2` | `degrade.sol[3]` | `#F26897` |
| `#F77B9C` | `degrade.sol[4]` | `#F77B92` |
| `#E28643` | `cor.laranja-selecao`, `degrade.sol[5]` | `#E29343` |
| `#F1AB7A` | `degrade.anel[0]` | `#F1B57A` |
| `#F67A9B` | `degrade.anel[1]` | `#F67A8D` |
| `#DE65AE` | `degrade.anel[2]` | `#DE65A4` |
| `#6A1A3C` | `cor.vinho` | `#6A1A35` |
| `#492842` | `cor.ameixa` | `#49283E` |
| `#755882` | `cor.malva-painel` | `#7B5882` |
| `#504161` | `cor.malva-escuro` | `#554364` |
| `#171717` | `cor.preto-barra` | `#1C171A` |
| `#2B2927` | `cor.chip-escuro` | `#2D252A` |
| `#2E2E2E` | `cor.disco-escuro` | `#33292F` |
| `#201C24` | `cor.tinta` | `#241E27` |
| `#E7A164` | `cor.laranja-texto-ativo` | `#E7AC64` |
| `#E247C6` | `cor.magenta` | `#E247B6` |
| `#FFFFFF` | `cor.branco` | `#FCFBFB` |
| `#FFCDEA` | `cor.rosa-valor` | `#FFCDE6` |
| `#FBE591` | `cor.amarelo-aviso` | `#FBEE91` |
| `#FE7594` | `cor.vida` | `#FE758D` |
| `#FFAD49` | `cor.energia` | `#FFBC49` |
| `#FE7B9E` | `cor.seta-jogador` | `#FE7B93` |
| `#F2B6FF` | `cor.marcador` | `#F8B6FF` |
| `#9599A8` | `cor.radar` | `#9295AB` |
| `#AC3844` | `cor.inimigo` | `#AC383A` |
| `#753538` | `cor.inimigo-mancha` | `#753935` |
| `#434967` | `cor.estrela-inativa` | `#434567` |
| `#FF74D8` | `cor.atributo-ganho` | `#FF74CC` |
| `#D13433` | `cor.atributo-perda` | `#D14133` |
| `#FA6DA1` | `cor.arco-item` | `#FA6D95` |
| `#8FBF7C` | `cor.mapa-parque` | `#89BF7C` |
| `#3F7181` | `cor.mapa-agua` | `#3F6C81` |
| `#84A07C` | `cor.apoio-salvia` | `#80A07C` |
| `#627197` | `cor.apoio-ardosia` | `#626D97` |
| `#A492BA` | `cor.apoio-lavanda` | `#A892BA` |
| `#719AC5` | `cor.apoio-ceu` | `#7193C5` |
| `#E77999` | `cor.apoio-rosa` | `#E77990` |
| `#B184AC` | `cor.apoio-lilas` | `#B184A8` |
| `#64B5CF` | `cor.apoio-ciano` | `#64ACCF` |
| `#BF52DB` | `cor.apoio-flamingo` | `#CA52DB` |
| `#A6699D` | `cor.onda-lilas` | `#A66998` |
| `#A06282` | `degrade.lista[0]` | `#A0627D` |
| `#D07178` | `degrade.lista[1]` | `#D07271` |
| `#181818` | `cor.preto-lateral` | `#201A1E` |
| `rgba(40,10,40,0.45)` | `sombra.apresentacao` | `rgba(44,12,48,0.45)` |

## Consequências
- **Positivas:** nenhum valor igual ao conceito; o visual continua o do prompt.
- **Negativas / Trade-offs:** quem ler o prompt e o `tokens.json` lado a lado vê hex diferentes; esta tabela explica.
- **Ações de acompanhamento:** prompts de imagem usam o BLOCO DE ESTILO com os hex deslocados (`ilustracao/estilo.txt`).
