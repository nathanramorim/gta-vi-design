# Módulos — costa-neon

Dependências apontam para `tokens`, sem ciclos (`ARQ-02`).

## tokens
**Responsabilidade:** casa única de cores, degradês, tipografia, espaçamento, raios e sombras; `tokens build` gera o CSS.

## validar
**Responsabilidade:** confere hex na lista do prompt, sombras roxas ou azuis, contorno ameixa, barras e linha neon nas telas, ausência de fonte ou nome associado a obra existente. Depende de `tokens`.

## fundamentos
**Responsabilidade:** página de amostras gerada dos tokens. Depende de `tokens`.

## componentes
**Responsabilidade:** componentes com estados normal, foco, ativo e desabilitado, só com variáveis CSS. Depende de `tokens`.

## telas
**Responsabilidade:** 8 telas 1920x1080 e `render telas` (HTML -> PNG). Depende de `componentes`.

## ilustracao
**Responsabilidade:** BLOCO DE ESTILO, receitas, listas de sorteio e `prompt` (6 modos). Depende de `tokens`.

## temas
**Responsabilidade:** export por consumidor (`tema carrossel|video|readme|forge-sdd`). Depende de `tokens`.
