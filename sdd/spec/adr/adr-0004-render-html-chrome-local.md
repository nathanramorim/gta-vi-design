# ADR-0004: Telas e pranchas renderizadas de HTML para PNG no Chrome local

- **Data:** 2026-11-19
- **Status:** `proposto`
- **Regras afetadas (IDs da constitution):** `ARQ-04`, Regra 11
- **Autor / Responsável:** dono do repositório

## Contexto
As 8 telas precisam sair em PNG 1920x1080 com fontes reais, desfoque e brilho. O carrossel-studio já resolveu isso com Playwright e o Chrome do sistema.

## Opções Consideradas
1. **Pillow desenhando à mão:** sem CSS, sem desfoque fácil, muito código.
2. **HTML/CSS com os tokens, PNG pelo Chrome local (Playwright):** o mesmo CSS serve de documentação e de imagem.

## Decisão
Opção 2, a confirmar no Gate 1. Versão do Playwright fixada na feature 04.

## Consequências
- **Positivas:** fidelidade; reúso do caminho do carrossel-studio.
- **Negativas / Trade-offs:** precisa de Chrome ou do Chromium do Playwright (entra no `requisitos.toml` na feature 04).
- **Ações de acompanhamento:** feature 04.
