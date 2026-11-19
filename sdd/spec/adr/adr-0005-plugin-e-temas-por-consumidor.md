# ADR-0005: Plugin/skill costa-neon e um tema exportado por consumidor

- **Data:** 2026-11-19
- **Status:** `proposto`
- **Regras afetadas (IDs da constitution):** `ARQ-03`, `ARQ-06`, `DUP-03`, Regras 3 e 12
- **Autor / Responsável:** dono do repositório

## Contexto
Outras ferramentas do dono já têm formato de marca: o carrossel-studio e o gerador de vídeos leem um "arquivo de marca" JSON (`cores`, `fontes`, `logo`; `.video-marca.json`), o readme-studio lê `docs/img/identidade.json`, e o Forge SDD prepara a "Edição Missões" da v5.0.0.

## Opções Consideradas
1. **Cada consumidor copia os hex:** diverge com o tempo.
2. **`tema <consumidor>` gera o arquivo no formato que cada um já lê, e o design system vira plugin/skill replicável:** reúso sem cópia.

## Decisão
Opção 2, a confirmar no Gate 1. Plugin em `plugins/costa-neon/` (como o carrossel-studio), com a skill chamando os scripts como ferramentas.

## Consequências
- **Positivas:** um tema, várias ferramentas; replicável para outro {SISTEMA}.
- **Negativas / Trade-offs:** acompanhar mudanças de formato dos consumidores (testes de contrato).
- **Ações de acompanhamento:** feature 06.
