# Padrão de Engenharia — Sankhya e desenvolvimento em geral

Conjunto de regras de engenharia prontas para alimentar Claude, ChatGPT, Claude Code e Codex, para que a IA siga sempre as mesmas boas práticas de desenvolvimento, segurança, banco de dados, testes e documentação — sem você repetir as instruções a cada conversa.

Inclui uma extensão dedicada ao **ecossistema Sankhya**, com a separação explícita entre personalização legada e Add-on Studio.

**Comece por [INSTALL.md](INSTALL.md).**

## Por que existe

Assistentes de IA escrevem código plausível, não código correto. No Sankhya isso aparece de forma específica: a IA inventa tabela, campo e API que não existem naquela instalação. Este repositório reduz esses erros dando ao assistente um conjunto de regras explícito e verificável.

## O que ele cobre

**Universal** — segurança, qualidade, testes, documentação, arquitetura, APIs, observabilidade, entrega e cadeia de suprimentos.

**Linguagens** — Java, C#, Go, Kotlin, Swift, Dart, PHP, C++, Python, TypeScript, JavaScript, Rust, PL/SQL.

**Dados** — Oracle, SQL Server, PostgreSQL, MySQL, MongoDB, Redis, modelagem e SQL.

**Front e back** — React, Next.js, Tailwind, Electron, HTML/CSS, Node.js.

**Sankhya** — Java legado (`AcaoRotinaJava`, Jape, `DynamicVO`, `NativeSql`), Add-on Studio (`@ActionButton`, `@Service`, `@Listener`), transações, regras de negócio, SQL nativo, logging, segurança, performance e documentação.

## Princípios

- Linguagem normativa MUST / SHOULD / MAY ([BCP 14](governance/requirement-levels.md)).
- Regras escritas com base em fontes primárias, com link para elas — sem copiar documentação de terceiros.
- Carregamento seletivo: só as regras da stack em uso entram no contexto.
- Regra mais específica prevalece sobre a mais genérica.

## Precedência

1. Requisito explícito da tarefa.
2. Convenções documentadas do projeto.
3. Regras da plataforma/framework.
4. Regras da linguagem.
5. Este padrão.
6. Boas práticas genéricas.

## Estrutura

```text
dist/core.md        núcleo condensado, para campos de instrução
dist/claude-rules/  regras por linguagem do Claude Code (geradas)
dist/web/           pacote para Projects e GPTs (gerado)
dist/local/         dicionário da instalação (gerado, não versionado)
governance/      níveis de requisito, hierarquia, exceções
security/        desenvolvimento seguro, segredos, threat modeling
quality/         qualidade de código
languages/       regras por linguagem
data/            bancos de dados e SQL
frontend/        web e desktop
backend/         serviços
api/             contratos HTTP
testing/         estratégia de testes
documentation/   documentação e comentários
architecture/    arquitetura e ADRs
delivery/        Git, CI/CD
observability/   logs, métricas, traces
supply-chain/    dependências e SBOM
stacks/          extensões de plataforma (Sankhya)
templates/       modelos de documento
checklists/      listas de revisão
adapters/        instruções curtas por assistente
references/      fontes primárias
```

## Sankhya: como usar

A extensão [stacks/java-sankhya/](stacks/java-sankhya/) **não deve ser aplicada a Java comum**. Antes de gerar código, o assistente precisa identificar o modelo do projeto:

- **Legado** — `AcaoRotinaJava`, `ContextoAcao`, `JapeSession`, `EntityFacade`, `DynamicVO`, `NativeSql`, JAR publicado por Módulo Java.
- **Add-on Studio** — `@Service`, `@ActionButton`, `@Listener`, `@Callback`, `@BusinessRule`, `@Transactional`, projeto Gradle.

Misturar os dois gera código que não compila no ambiente alvo. Ver [stacks/java-sankhya/README.md](stacks/java-sankhya/README.md).

## Contribuindo

Ver [CONTRIBUTING.md](CONTRIBUTING.md). Regra específica de plataforma precisa vir acompanhada da versão do Sankhya em que foi verificada — padrão sem evidência vira folclore.

## Licença

[MIT](LICENSE). As regras aqui são texto próprio; a documentação oficial de terceiros é referenciada por link, nunca copiada.
