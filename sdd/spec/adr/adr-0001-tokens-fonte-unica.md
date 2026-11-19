# ADR-0001: tokens.json é a fonte única; CSS, temas e telas são gerados

- **Data:** 2026-11-19
- **Status:** `aprovado`
- **Regras afetadas (IDs da constitution):** `DUP-01`, `DUP-04`, Regra 8
- **Autor / Responsável:** dono do repositório

## Contexto
O prompt do diretor de arte lista dezenas de hex exatos. Se cada tela, tema ou consumidor copiar valores à mão, eles divergem (o mesmo laranja vira `#E28643` num lugar e `#E28642` em outro).

## Opções Consideradas
1. **CSS escrito à mão como fonte:** simples, mas os consumidores (vídeo, carrossel, README) não leem CSS.
2. **`tokens.json` como fonte, CSS e temas gerados por script:** um valor muda em um lugar só.

## Decisão
Opção 2. `tokens/costa-neon.tokens.json` guarda cores, degradês, tipografia, espaçamento, raios e sombras. `tokens build` gera `costa-neon.css`; `tema <consumidor>` gera o arquivo de cada consumidor; `validar` confere que nada usa hex fora da lista.

## Consequências
- **Positivas:** consistência; validação automática.
- **Negativas / Trade-offs:** o CSS gerado não deve ser editado à mão.
- **Ações de acompanhamento:** feature 01 (tokens + validar).
