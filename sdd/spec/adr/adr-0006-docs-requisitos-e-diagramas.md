# ADR-0006: README pelo readme-studio, requisitos pelo motor v0.1.0, diagramas pelo diagram-studio

- **Data:** 2026-11-19
- **Status:** `aprovado`
- **Regras afetadas (IDs da constitution):** `FLX-07`, Regras 12 e 13
- **Autor / Responsável:** dono do repositório

## Contexto
Os repositórios do dono seguem um padrão: README comercial com `## Requisitos` e um bloco "Cole isto na sua IA" que usa um script como ferramenta, e diagramas em imagem conferidos.

## Opções Consideradas
1. **README e diagramas à mão:** inconsistente, prompt genérico.
2. **readme-studio (`readme-comercial`) + motor requisitos-para-ia v0.1.0 vendorizado + skill `diagramas-c4-mermaid` com motor diagram-studio:** padrão verificável.

## Decisão
Opção 2. `scripts/requisitos.py`, `bootstrap.sh` e `bootstrap.ps1` copiados sem edição da tag `v0.1.0` (`skills.lock` com commit e sha256); `requisitos.toml` na raiz. Diagramas em JSON em `docs/diagramas/`, renderizados em SVG e PNG escuros. Se o diagram-studio faltar, usar Mermaid e dizer isso no PR.

## Consequências
- **Positivas:** README passa no `verificar_readme.py`; diagramas legíveis.
- **Negativas / Trade-offs:** o diagram-studio não está instalado como plugin nesta máquina; usado a partir do repositório público (commit no PR).
- **Ações de acompanhamento:** feature 07 refaz o README com as telas reais.
