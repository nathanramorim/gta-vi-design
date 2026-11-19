<p align="center">
  <img src="docs/banner.svg" alt="costa-neon: tokens, componentes, telas e prompts de imagem num tema único para as suas ferramentas" width="100%">
</p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/status-em%20constru%C3%A7%C3%A3o-FE7693?labelColor=171717">
  <img alt="fase" src="https://img.shields.io/badge/fase-discovery%20(Gate%201)-FDAA6C?labelColor=171717">
  <img alt="python via uv" src="https://img.shields.io/badge/python-via%20uv-E851AB?labelColor=171717">
</p>

<h3 align="center">Tokens, componentes, telas e prompts de imagem<br>num tema único para as suas ferramentas.</h3>

---

## O que é

**Costa Neon** é um design system de pôr do sol tropical: céu rosa, laranja e roxo, palmeiras em silhueta, art déco em tons pastel e neon. Ele vai entregar:

- **tokens** (cores, degradês, tipografia, espaçamento, raios e sombras) em JSON e em variáveis CSS;
- uma **página de fundamentos** com amostras;
- **componentes** com os estados normal, foco, ativo e desabilitado;
- **8 telas de referência** em 1920x1080;
- um **guia de ilustração** que monta prompts de imagem sem inventar nada;
- um **tema pronto** para outras ferramentas (carrossel, vídeo, banner de README e o Forge SDD).

É replicável: você troca `{SISTEMA}`, `{MARCA}`, `{CIDADE}`, `{IDIOMA}` e `{FORMATO}` e tem o seu. Tudo é original: nenhum logo, nome, personagem, mapa ou fonte de jogo, filme ou marca existente.

> **Status: em construção.** Por enquanto o repositório tem só a discovery (o plano) e as decisões. Nada de tokens ou telas ainda. Veja [`sdd/discovery/01-costa-neon/`](sdd/discovery/01-costa-neon/discovery.md).

## Por que usar

| | |
|---|---|
| **Um valor, um lugar** | Cada cor existe uma vez, no `tokens.json`. CSS, telas e temas saem dele. |
| **A IA não chuta cor** | Ela usa scripts (`validar`, `prompt`, `tema`) como ferramentas e recebe sempre o mesmo resultado. |
| **Original de verdade** | Fontes abertas (display Bowlby One), nomes inventados, HUD com desenho próprio. |
| **Roda em qualquer sistema** | macOS, Linux e Windows, Python só pelo `uv`. |

## Requisitos

Hoje o repositório só precisa do `uv` (para rodar o script de requisitos) e, por ser privado, do acesso ao GitHub. Navegador, fontes e pacotes Python entram quando os scripts existirem; esta seção cresce junto.

> **Cole isto na sua IA antes de instalar:**
>
> "Confira os requisitos do costa-neon. Se o repositório ainda não estiver clonado, clone com o GitHub CLI: `gh repo clone nathanramorim/costa-neon` (instale o gh com `winget install --id GitHub.cli -e` no Windows, pelo https://cli.github.com no macOS e pelo pacote `gh` da sua distro no Linux; o `gh auth login` é comigo). No Windows, rode `powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1`; no macOS ou Linux, rode `sh scripts/bootstrap.sh`. Ele confere e, com o meu ok, instala o uv, e depois mostra o que falta. Para cada item, peça meu ok e rode `uv run scripts/requisitos.py instalar --sim <item>`. Itens marcados como é com você (licença, consentimento ou voz, login, permissões do sistema, senha de administrador): me explique e espere eu fazer. Não aceite licenças nem declarações por mim e não mexa em senhas, chaves ou tokens."

| | O que precisa | Detalhe |
|---|---|---|
| **Onde roda** | macOS, Linux e Windows | A receita de requisitos cobre os 3 sistemas (`uv run scripts/requisitos.py validar`). Testado até agora só no macOS (arm64) com Claude Code; o CI nos 3 sistemas entra com o primeiro código. |
| **Programas** | `uv` 0.8 ou mais novo (obrigatório); `git` 2.0+ e `gh` (para clonar o repositório privado) | `uv run scripts/requisitos.py checar` confere tudo e diz o que falta. Python sempre pelo [`uv`](https://docs.astral.sh/uv/). |
| ↳ macOS | `sh scripts/bootstrap.sh` | Instalador oficial do `uv` (sem sudo), com o seu ok; Homebrew é só uma opção, se você já tiver. |
| ↳ Linux | `sh scripts/bootstrap.sh` | Instalador oficial do `uv`; `pacman` ou `dnf` quando houver. `git` e `gh` pelo gerenciador da distro. |
| ↳ Windows | `powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1` | Instalador oficial do `uv`, ou `winget`, `scoop` e `choco`. O `winget` pede a você o aceite dos termos. |
| **Downloads na primeira execução** | Nenhum por enquanto | Quando as telas existirem: fontes abertas do fontsource em `~/.cache/costa-neon/fontes`, uma vez. |
| **Contas e chaves** | Conta no GitHub com acesso a este repositório privado | `gh auth login` é com você; a IA nunca digita senha nem token. Nenhuma chave fica no repositório. |
| **Máquina** | Qualquer computador que rode o `uv` | Sem requisito de memória ou GPU nesta fase. |
| **Licenças e limites de uso** | Fontes previstas, todas OFL-1.1 | Bowlby One, Josefin Sans, Outfit, Kaushan Script, Zilla Slab, Anton e Oswald (conferido no fontsource em 19/11/2026). |
| **O que você fornece** | Os valores de `{MARCA}` e `{CIDADE}` (inventados) | Foto de pessoa só com autorização dela, só adultos, sem figuras públicas. |

## Instalação

Por enquanto, só clonar e conferir os requisitos:

```bash
gh repo clone nathanramorim/costa-neon
cd costa-neon
uv run scripts/requisitos.py checar
```

O plugin `costa-neon` (para pedir telas, temas e prompts em conversa) vem depois do Gate 1.

## Como usar

Ainda não há comandos de design. O que existe hoje:

| Quero | Onde |
|---|---|
| Ler a fonte de verdade do estilo | [`docs/prompt-diretor-de-arte.md`](docs/prompt-diretor-de-arte.md) |
| Ver o plano e as perguntas em aberto | [`sdd/discovery/01-costa-neon/discovery.md`](sdd/discovery/01-costa-neon/discovery.md) |
| Ver os critérios e a arquitetura | [`sdd/discovery/01-costa-neon/criteria.md`](sdd/discovery/01-costa-neon/criteria.md) |
| Ver as decisões (ADRs) | [`sdd/spec/adr/`](sdd/spec/adr/) |

Comandos planejados (ainda não existem): `tokens build`, `validar`, `render telas`, `prompt` e `tema <consumidor>`.

<p align="center">
  <img src="docs/diagramas/c4-conteineres.svg" alt="Contêineres do Costa Neon: tudo nasce do tokens.json e o resto é gerado por script" width="100%">
</p>

## Segurança e privacidade

- Nenhum segredo no repositório; nada é enviado para fora pelos scripts.
- Prompts de imagem nunca citam obra, marca ou personagem existente.
- Foto de pessoa só com autorização dela, só adultos, sem figuras públicas. A autorização é sua, nunca da IA.

## Versões

| Versão | Novidades |
|---|---|
| 0.1.0 (planejada) | Discovery do design system; ainda sem tag. |

## Licença

Ainda não definida (repositório privado). As fontes previstas são todas OFL-1.1.
