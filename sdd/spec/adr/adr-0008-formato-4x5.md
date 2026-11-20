# ADR-0008: Formato 4:5 (1080x1350) para peças de letreiro

- **Data:** 2026-11-20
- **Status:** `aprovado` (pedido do dono em 20/11/2026, resposta "faz o recomendado")
- **Regras afetadas (IDs da constitution):** Regra 15, `SEG-01`, `GOV-01`
- **Autor / Responsável:** dono do repositório

## Contexto
A Regra 15 aceitava `{FORMATO}` só em `16:9|1:1|9:16`. A iniciativa 02 entrega a peça de letreiro (cartaz e post de Instagram) e o formato do post é 4:5. A 02-04 já aceita `4:5` em `render peca`; a Camada B r1 marcou a divergência como `duvida`.

## Opções Consideradas
1. **Remover o 4:5 da peça:** cumpre a regra, mas perde o formato do post.
2. **Incluir o 4:5 na lista de `{FORMATO}`:** a validação de borda passa a aceitar 4:5 em todo o repositório.

## Decisão
Opção 2. `{FORMATO}` passa a ser `16:9|1:1|9:16|4:5`; 4:5 mede 1080x1350. Nada mais da Regra 15 muda, e as Regras 4 e 8 e a ADR-0002 seguem intactas.

## Consequências
- **Positivas:** a peça do post sai no formato certo, sem exceção solta no código.
- **Negativas / Trade-offs:** `entrada.formato` e `prompt` passam a aceitar 4:5 (ajuste de código e teste a cargo da 02).
- **Ações de acompanhamento:** alinhar `entrada.py` à lista nova e remover a exceção local de `render peca`.
