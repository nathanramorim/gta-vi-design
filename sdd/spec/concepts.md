# Catálogo de Conceitos e Contratos (`DUP-01`) — costa-neon

| Conceito | Dono | Entidade | Contrato público | Observação |
| --- | --- | --- | --- | --- |
| Token de design | `tokens/` | `costa-neon.tokens.json` | `tokens build` | Fonte única (ADR-0001) |
| Lista de hex permitidos | `tokens/` | todos os hex do prompt | `validar` | Nada fora dela |
| Tema de consumidor | `temas/` | um arquivo por consumidor | `tema <consumidor>` | Gerado, nunca editado à mão |
| Prompt de imagem | `ilustracao/` | BLOCO DE ESTILO + receita + variáveis | `prompt` | Sem nome de obra existente |
| Requisitos | `scripts/requisitos.py` | `requisitos.toml` | `checar`, `instalar`, `prompt` | Motor vendorizado v0.1.0 |
