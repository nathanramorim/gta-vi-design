# ADR-0002: Originalidade, propriedade intelectual e fontes abertas

- **Data:** 2026-11-19
- **Status:** `aprovado`
- **Regras afetadas (IDs da constitution):** Regras 4, 5 e 11, `GOV-01`
- **Autor / Responsável:** dono do repositório

## Contexto
O universo do Costa Neon lembra um gênero conhecido (mundo aberto em cidade costeira ao pôr do sol). O prompt original sugere "Pricedown Black" como display padrão; essa fonte é fortemente associada ao logotipo de uma série de jogos existente. HUD, radar, estrelas de alerta, dinheiro e rodas de seleção e de rádio são convenções do gênero, mas a disposição exata e a iconografia de um jogo específico não são nossas. A paleta do prompt é quase igual, hex a hex, à medida de um conceito de fã publicado com todos os direitos reservados (registrado na discovery 0001).

## Opções Consideradas
1. **Seguir o prompt ao pé da letra (Pricedown padrão):** fiel ao texto, mas associa o sistema a marca de terceiros e a uma fonte sem licença aberta clara.
2. **Fontes abertas como padrão e regras de originalidade escritas:** reconhecível pelo clima, sem copiar marca.

## Decisão
Opção 2.
- **Display padrão: Bowlby One (OFL-1.1).** Pricedown fica fora dos padrões, da pilha de fallback e dos exemplos da documentação.
- Demais papéis, todos OFL-1.1 conforme a API do fontsource em 2026-11-19: texto Josefin Sans (alternativa Outfit), script Kaushan Script, slab Zilla Slab, título gigante Anton, HUD Oswald. Baixadas do fontsource para cache local, nunca versionadas no repositório.
- HUD e rodas: layout, ícones e proporções desenhados por nós, com a paleta do repositório; nunca replicar layout ou ícone de um jogo existente.
- Nomes de cidade, bairro, rádio e marca sempre inventados; prompts de imagem nunca citam obra, marca ou personagem existente.
- Foto de pessoa só com autorização, só adultos, sem figuras públicas.
- `docs/prompt-diretor-de-arte.md` fica literal (é texto do dono); esta ADR prevalece onde ele diverge.

## Consequências
- **Positivas:** uso comercial e público sem risco de marca; fontes redistribuíveis.
- **Negativas / Trade-offs:** Bowlby One não tem o mesmo desenho do letreiro de referência (é intencional).
- **Ações de acompanhamento:** `validar` reprova "Pricedown" em tokens, CSS e docs (exceto o prompt literal e esta ADR); revisão de PI por peça.
