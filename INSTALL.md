# Instalação

Escolha o canal conforme onde você programa. Você pode usar mais de um.

| Onde você usa IA | O que instalar | Confiabilidade |
|---|---|---|
| Claude Code (terminal/VS Code) | repositório no disco | alta — lido a cada sessão |
| Codex CLI | repositório no disco | alta |
| Claude.ai (web/desktop) | Project com instruções + `dist/web/` | alta dentro do Project |
| ChatGPT | Project ou GPT com instruções + `dist/web/` | alta dentro do Project |
| Caixa de "instruções personalizadas" | apenas o `dist/core.md` | média — texto curto, sempre ativo |
| Memória do assistente | apenas uma frase de roteamento | baixa — o modelo decide quando lembrar |

> Regra geral: **o conteúdo mora em arquivos, não na memória.** A memória serve para lembrar o assistente de ir buscar o padrão.

---

## Claude Code via plugin (caminho mais curto)

Funciona igual em Linux, macOS e Windows, e é o modo recomendado depois que o
repositório estiver no GitHub. Dentro de uma sessão do Claude Code:

```
/plugin marketplace add isaacoolibama/engineering-standards-starter
/plugin install engineering-standards@engineering-standards
```

Ou pelo terminal, antes de abrir a sessão:

```bash
claude plugin marketplace add isaacoolibama/engineering-standards-starter
claude plugin install engineering-standards@engineering-standards
```

Isso entrega quatro skills, que carregam sob demanda:

| Skill | Quando dispara |
|---|---|
| `sankhya` | ao trabalhar com personalização Sankhya |
| `verificar-dicionario` | antes de citar tabela ou campo do Sankhya |
| `revisar` | ao pedir revisão de código contra o padrão |
| `instalar-regras` | manual |

**Um passo a mais:** o plugin não instala sozinho as regras por linguagem, porque
`paths:` não é componente de plugin. Rode uma vez:

```
/engineering-standards:instalar-regras
```

### A partir de um clone local (desenvolvimento)

```bash
claude plugin marketplace add /caminho/absoluto/do/repositorio
claude plugin install engineering-standards@engineering-standards
```

O caminho precisa ser absoluto ou começar com `./` — `.` sozinho é recusado.

### Publicar alterações no plugin

Depois de mexer nas regras ou nas skills:

```bash
python3 scripts/build-rules.py                     # regenera dist/claude-rules/ e plugins/*/rules/
python3 scripts/build-web.py                       # regenera dist/web/ (Projects e GPTs)
claude plugin validate ./plugins/engineering-standards
```

Suba a versão em `plugins/engineering-standards/.claude-plugin/plugin.json` para que
quem já instalou receba a atualização.

---

## Linux e macOS

### Baixar

```bash
git clone https://github.com/isaacoolibama/engineering-standards-starter.git ~/engineering-standards
```

### Claude Code — todos os projetos

```bash
mkdir -p ~/.claude
cat ~/engineering-standards/dist/core.md >> ~/.claude/CLAUDE.md
```

O arquivo `~/.claude/CLAUDE.md` é lido em toda sessão, em qualquer pasta.

### Claude Code — regras por linguagem, em todos os projetos

O passo acima instala só o núcleo. As regras por linguagem ficam em `~/.claude/rules/`,
que o Claude Code lê em qualquer projeto da máquina:

```bash
cd ~/engineering-standards && python3 scripts/build-rules.py
mkdir -p ~/.claude/rules
ln -sfn ~/engineering-standards/dist/claude-rules ~/.claude/rules/engineering-standards
```

O symlink faz um `git pull` no repositório atualizar as regras sozinho.

Cada regra tem `paths:` no cabeçalho e **só entra no contexto quando você mexe em
arquivo daquele tipo** — a regra de Go não ocupa espaço enquanto você escreve Python.

### Claude Code — um projeto específico

```bash
cd /caminho/do/seu/projeto
ln -s ~/engineering-standards/CLAUDE.md CLAUDE.md
```

### Codex CLI

```bash
mkdir -p ~/.codex
cp ~/engineering-standards/dist/core.md ~/.codex/AGENTS.md
```

Para um projeto específico, copie o `AGENTS.md` da raiz do repositório para a raiz do seu projeto.

O Codex lê, nesta ordem: `~/.codex/AGENTS.override.md` → `~/.codex/AGENTS.md` → os `AGENTS.md` do projeto (da raiz do repositório até a pasta atual). Arquivos mais próximos do código aparecem depois no prompt e prevalecem sobre os anteriores.

### Atualizar

```bash
cd ~/engineering-standards && git pull
```

---

## Windows

### Baixar (PowerShell)

```powershell
git clone https://github.com/isaacoolibama/engineering-standards-starter.git "$env:USERPROFILE\engineering-standards"
```

Sem Git instalado: baixe o ZIP pelo botão **Code → Download ZIP** no GitHub e extraia em `%USERPROFILE%\engineering-standards`.

### Claude Code — todos os projetos

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude" | Out-Null
Get-Content "$env:USERPROFILE\engineering-standards\dist\core.md" |
  Add-Content "$env:USERPROFILE\.claude\CLAUDE.md"
```

### Claude Code — um projeto específico

Copie os arquivos (links simbólicos no Windows exigem privilégio de administrador):

```powershell
cd C:\caminho\do\seu\projeto
Copy-Item "$env:USERPROFILE\engineering-standards\CLAUDE.md" .
Copy-Item "$env:USERPROFILE\engineering-standards\.claude" . -Recurse
```

### Claude Code — regras por linguagem, em todos os projetos

```powershell
cd "$env:USERPROFILE\engineering-standards"; python scripts\build-rules.py
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\rules" | Out-Null
Copy-Item "$env:USERPROFILE\engineering-standards\dist\claude-rules" `
          "$env:USERPROFILE\.claude\rules\engineering-standards" -Recurse -Force
```

No Windows a cópia é mais simples que o link simbólico, que exige privilégio de
administrador. Em compensação, repita o comando depois de cada `git pull`.

### Codex CLI

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex" | Out-Null
Copy-Item "$env:USERPROFILE\engineering-standards\dist\core.md" "$env:USERPROFILE\.codex\AGENTS.md"
```

### WSL

Se você programa dentro do WSL, siga as instruções de **Linux** dentro dele. O `~/.claude` do Windows e o do WSL são separados — instalar em um não vale para o outro.

---

## IAs na web

Os nomes dos menus mudam com o tempo; o caminho geral se mantém.

### Passo 1 — gerar o pacote web

```bash
python3 scripts/build-web.py
```

| Saída | O que é | Quando usar |
|---|---|---|
| `dist/web/bundles/` | 5 arquivos, um por perfil de trabalho | limite baixo de arquivos, ou quando você quer só o recorte da sua stack |
| `dist/web/standards/` | 69 arquivos, um por documento | plataforma que aceita dezenas de arquivos e você quer granularidade |

Os bundles são `nucleo.md`, `sankhya.md`, `backend.md`, `frontend.md` e `linguagens.md`.
Cada um já embute o núcleo, então basta subir o da sua stack — ou `nucleo.md` sozinho,
se você quer só as regras transversais.

**Não suba as pastas do repositório direto.** Sete documentos se chamam `standard.md` e
quatro se chamam `java.md`; o knowledge base mostra só o nome do arquivo, sem a pasta, e
a lista fica ilegível. É esse achatamento que o `build-web.py` resolve — nele o caminho
vira prefixo (`backend-standard.md`, `stacks-java-sankhya-jape.md`).

**Não suba `dist/claude-rules/` nem `plugins/*/rules/`.** São cópias derivadas dos mesmos
documentos, geradas para o Claude Code, com frontmatter `paths:` que só ele interpreta.
Subir os dois conjuntos duplica o padrão dentro do knowledge base.

### Passo 2 — escolher o texto de instruções

| Situação | Texto para colar |
|---|---|
| Campo de instruções, sem arquivos anexados | `dist/core.md` |
| Project ou GPT do ChatGPT, com arquivos | `adapters/chatgpt-project-instructions.md` |
| Project do Claude, com arquivos | `adapters/claude-project-instructions.md` |
| Preferências pessoais do perfil (Claude) | `dist/core.md` ou `adapters/claude-profile.md` |

O `dist/core.md` é o padrão condensado: serve onde **não há** arquivo para consultar.
Os adapters são texto de roteamento — pressupõem os arquivos anexados e dizem ao
assistente como encontrar o documento certo. Não cole os dois; escolha pela linha da
tabela.

### Claude — claude.ai

**Opção A — Project (recomendada, é onde cabe tudo)**

1. Menu lateral → **Projects** → **Create project**.
2. Nomeie (ex.: "Desenvolvimento Sankhya").
3. Em **Instructions** (ou "Set project instructions"), cole `adapters/claude-project-instructions.md`.
4. Em **Project knowledge** → **Add content**, envie os arquivos de `dist/web/bundles/`
   (ou os de `dist/web/standards/` que interessam à sua stack).
5. Converse sempre **dentro desse Project**. Fora dele, as instruções não valem.

**Opção B — preferências pessoais (valem em todas as conversas)**

1. Ícone do perfil → **Settings** → **Profile**.
2. No campo de preferências pessoais, cole `dist/core.md`.
3. Salve.

É o único canal que vale em toda conversa, mas comporta pouco texto — por isso só o núcleo.

### ChatGPT — chatgpt.com

**Opção A — Instruções personalizadas (valem em todas as conversas)**

1. Ícone do perfil → **Configurações** → **Personalização**.
2. Abra **Instruções personalizadas**.
3. No campo "O que mais o ChatGPT deveria saber sobre você?", cole `dist/core.md`.
4. Ative e salve.

O campo aceita cerca de 1.500 caracteres — o `dist/core.md` foi dimensionado para caber.

**Opção B — Project (cabe muito mais)**

1. Menu lateral → **Projects** → novo projeto.
2. Em **Instruções**, cole `adapters/chatgpt-project-instructions.md`.
3. Em **Arquivos**, envie `dist/web/bundles/`.

**Opção C — GPT personalizado (para compartilhar com a equipe)**

1. Menu lateral → **GPTs** → **Criar**.
2. Aba **Configure** → campo **Instructions**: cole `adapters/chatgpt-project-instructions.md`
   (o limite aqui é bem maior que o das instruções personalizadas).
3. Em **Knowledge**, envie `dist/web/bundles/`.
4. Em compartilhamento, escolha link ou workspace.

> Os limites de quantidade e tamanho de arquivo de cada plataforma mudam com o tempo e
> com o plano contratado. Se o upload dos bundles for recusado, suba primeiro
> `nucleo.md` e o bundle da sua stack — é o mínimo que mantém o padrão útil.

### Gemini — gemini.google.com

Use **Gems**: crie um Gem, cole `dist/core.md` nas instruções e anexe os bundles de
`dist/web/bundles/`.

### Memória do assistente

Não cole o padrão inteiro na memória. Peça apenas a regra de roteamento:

> "Lembre-se: em toda tarefa de desenvolvimento, aplicar o meu Padrão de Engenharia — identificar a stack antes de codificar, nunca inventar API/tabela/campo, SQL sempre parametrizado, responder em português."

---

## Verificar se funcionou

### No Claude Code (verificação exata)

Abra uma sessão nova e rode:

| Comando | O que mostra |
|---|---|
| `/context` | quais arquivos de instrução **realmente** entraram no contexto — se não aparecer aqui, não está valendo |
| `/memory` | lista e abre os arquivos de memória de cada escopo |

O `~/.claude/CLAUDE.md` deve aparecer sob **Memory files**. As regras com `paths:`
só aparecem depois que você abre um arquivo do tipo correspondente — abra um `.java`
e rode `/context` de novo para ver a regra de Java entrar.

### Nos assistentes web

Abra uma conversa nova e peça:

> "Escreva uma função que busca um usuário por e-mail no banco."

Sinais de que o padrão está ativo:

- respondeu em português;
- perguntou qual linguagem/banco antes de assumir;
- usou consulta parametrizada sem você pedir;
- não inventou nome de tabela ou campo.

Se nada disso aconteceu, o texto não está sendo carregado — confira se salvou no campo certo e, no caso de Projects, se a conversa está dentro do projeto.

## Manutenção

Antes de publicar qualquer alteração no padrão:

```bash
python3 scripts/build-rules.py   # regenera as regras do Claude Code
python3 scripts/build-web.py     # regenera o pacote das IAs web
scripts/validate.sh              # estrutura + links internos
LINK_CHECK=1 scripts/validate.sh # inclui checagem HTTP de todas as fontes
```

Fonte que sai do ar deve ser substituída, não mantida quebrada — foi o que aconteceu com o guia Trivadis de PL/SQL, arquivado e removido do ar.
