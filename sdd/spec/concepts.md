# Catálogo de Conceitos e Contratos (`DUP-01`) — costa-neon

| Conceito | Dono | Entidade | Contrato público | Observação |
| --- | --- | --- | --- | --- |
| Token de design | `plugins/costa-neon/skills/costa-neon/tokens/` | `costa-neon.tokens.json` | `tokens build` | Fonte única (ADR-0001) |
| Lista de hex permitidos | `plugins/costa-neon/skills/costa-neon/tokens/` | todos os hex do `tokens.json` (ADR-0007) | `validar` | Nada fora dela |
| Tema de consumidor | `temas/` | um arquivo por consumidor | `tema <consumidor>` | Gerado, nunca editado à mão |
| Prompt de imagem | `ilustracao/` | BLOCO DE ESTILO + receita + variáveis | `prompt` | Sem nome de obra existente |
| Requisitos | `scripts/requisitos.py` | `requisitos.toml` | `checar`, `instalar`, `prompt` | Motor vendorizado v0.1.0 |
