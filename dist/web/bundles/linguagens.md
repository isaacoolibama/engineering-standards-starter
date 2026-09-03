# Engineering Standards — linguagens

Convenções por linguagem.

## Núcleo

Responda sempre em português do Brasil.

Antes de escrever ou alterar código:
1. Identifique linguagem, framework, runtime, banco e as convenções já usadas no projeto.
2. Aplique somente as regras da stack em uso.
3. Não invente API, tabela, campo, biblioteca ou recurso de plataforma. Se não puder confirmar, diga que não confirmou.
4. Preserve o comportamento fora do escopo pedido; não refatore por conta própria.

Segurança (obrigatório):
- Toda entrada externa é não confiável.
- SQL sempre parametrizado, nunca concatenado.
- Nenhum segredo no código-fonte.
- Autorização validada no servidor, nunca apenas na interface.
- Nenhuma falha silenciosa: erro não pode ser engolido.

Qualidade:
- Função com responsabilidade única e nome que revela intenção.
- Teste proporcional ao risco; correção de bug acompanha teste de regressão.
- Comentário explica o porquê, não o quê.
- Mudança pequena, verificável e reversível.
- Documentação afetada é atualizada junto.

Sankhya: identifique primeiro se o projeto é legado (AcaoRotinaJava, Jape, DynamicVO, NativeSql) ou Add-on Studio (@ActionButton, @Service, @Listener). Nunca misture os dois modelos. Nunca cite tabela ou campo sem confirmar no dicionário de dados (TDDTAB/TDDCAM).

---

<!-- languages/cpp.md -->

# C++

Fontes primárias: [ISO C++](https://isocpp.org/), [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines.html).

## Ferramentas

- SHOULD usar `clang-format` e `clang-tidy` com configuração versionada.
- SHOULD compilar com `-Wall -Wextra` e tratar avisos relevantes como erro.
- SHOULD usar sanitizers (ASan/UBSan/TSan) na suíte de testes.
- MUST declarar o padrão da linguagem no build (`-std=`/`CMAKE_CXX_STANDARD`).

## Gerenciamento de recursos

- MUST seguir RAII; recursos MUST ser liberados por destrutor.
- MUST NOT usar `new`/`delete` explícitos em código novo — usar `std::unique_ptr`/`std::make_unique`.
- `shared_ptr` SHOULD ser usado apenas quando a propriedade for realmente compartilhada.
- MUST respeitar a regra de zero/três/cinco.

## Segurança de memória

- MUST NOT retornar referência ou ponteiro para objeto local.
- MUST NOT usar iterador ou referência após invalidação do container.
- SHOULD usar `std::span`/`std::string_view` em vez de ponteiro + tamanho, atentando ao tempo de vida.
- MUST NOT usar funções C inseguras (`strcpy`, `sprintf`, `gets`).
- Conversões SHOULD usar casts nomeados; MUST NOT usar cast estilo C.

## Design

- `const` SHOULD ser o padrão em parâmetros e métodos.
- SHOULD preferir algoritmos da biblioteca padrão a laços manuais.
- Exceções SHOULD ser lançadas por valor e capturadas por referência const.

---

<!-- languages/csharp.md -->

# C# / .NET

Fontes primárias: [C# Coding Conventions](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions), [Framework Design Guidelines](https://learn.microsoft.com/dotnet/standard/design-guidelines/), [.NET analyzers](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/overview).

## Ferramentas

- SHOULD versionar `.editorconfig` como fonte de estilo do projeto.
- SHOULD habilitar `EnableNETAnalyzers` e tratar avisos relevantes como erro no CI.
- Projetos novos SHOULD habilitar `<Nullable>enable</Nullable>`.

## Convenções

- Tipos, métodos e propriedades: PascalCase. Parâmetros e locais: camelCase. Campos privados: `_camelCase`.
- Interfaces: prefixo `I`.
- MUST NOT abreviar nomes de forma não convencional.
- APIs públicas SHOULD ter documentação XML quando o contrato não for óbvio.

## Assíncrono

- MUST NOT usar `async void`, exceto em event handlers.
- MUST NOT bloquear com `.Result` ou `.Wait()` em código assíncrono.
- SHOULD propagar `CancellationToken` em toda a cadeia.
- Bibliotecas SHOULD usar `ConfigureAwait(false)` quando não dependerem de contexto de sincronização.

## Recursos e erros

- `IDisposable` MUST ser consumido com `using`.
- MUST NOT capturar `Exception` genérica sem relançar ou tratar deliberadamente.
- MUST NOT usar `throw ex;` — usar `throw;` para preservar o stack trace.
- `HttpClient` SHOULD ser reutilizado via `IHttpClientFactory`, não instanciado por chamada.

## Dados

- MUST usar consultas parametrizadas; MUST NOT concatenar SQL.
- Entity Framework: SHOULD usar `AsNoTracking` em leitura pura e evitar N+1 por carregamento explícito.

---

<!-- languages/dart.md -->

# Dart / Flutter

Fontes primárias: [Effective Dart](https://dart.dev/effective-dart), [Linter rules](https://dart.dev/tools/linter-rules).

## Ferramentas

- MUST usar `dart format`.
- SHOULD habilitar `package:lints` ou `package:flutter_lints` em `analysis_options.yaml`.
- MUST manter `dart analyze` sem erros no CI.

## Estilo e tipos

- Classes e enums: UpperCamelCase. Membros e variáveis: lowerCamelCase. Arquivos: snake_case.
- SHOULD anotar tipos em APIs públicas; MUST NOT usar `dynamic` como atalho para tipagem.
- MUST habilitar null safety e evitar `!` sem garantia.
- SHOULD preferir `final`/`const` a variáveis mutáveis.

## Assíncrono

- Todo `Future` MUST ser aguardado ou ter erro tratado; MUST NOT deixar future não observado.
- SHOULD usar `unawaited()` quando o descarte for intencional.
- Streams MUST ter subscriptions canceladas no `dispose`.

## Flutter

- `build` MUST ser puro e barato; MUST NOT executar I/O ou lógica cara durante o build.
- SHOULD preferir widgets `const` quando possível.
- Controllers, listeners e timers MUST ser liberados em `dispose`.
- Estado SHOULD ficar fora do widget quando compartilhado entre telas.

---

<!-- languages/go.md -->

# Go

Fontes primárias: [Go Spec](https://go.dev/ref/spec), [Effective Go](https://go.dev/doc/effective_go), [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments).

## Formatação e ferramentas

- MUST usar `gofmt`/`goimports`; formatação não é assunto de revisão.
- SHOULD executar `go vet` e um agregador como `golangci-lint` no CI.
- MUST manter `go.mod` com a versão de Go realmente suportada pelo build.

## Erros

- Erros MUST ser tratados ou explicitamente propagados; MUST NOT descartar com `_` sem justificativa comentada.
- SHOULD envolver com `fmt.Errorf("contexto: %w", err)` para preservar a cadeia.
- MUST usar `errors.Is`/`errors.As` na comparação, não igualdade de string.
- `panic` SHOULD ficar restrito a erro de programação irrecuperável, não a fluxo esperado.

## Concorrência

- Toda goroutine MUST ter término previsível; MUST NOT deixar goroutine órfã.
- `context.Context` SHOULD ser o primeiro parâmetro em operações canceláveis e MUST NOT ser armazenado em struct.
- Canais SHOULD ser fechados por quem escreve, nunca por quem lê.
- Estado compartilhado MUST ser protegido por mutex ou confinado a uma goroutine.
- SHOULD executar testes com `-race` no CI.

## API e design

- Interfaces SHOULD ser declaradas no consumidor, pequenas e focadas.
- SHOULD retornar tipos concretos e aceitar interfaces.
- Identificadores exportados MUST ter doc comment iniciando pelo próprio nome.
- SHOULD preferir zero value útil a construtores obrigatórios.
- MUST fechar recursos com `defer` imediatamente após a aquisição.

---

<!-- languages/java.md -->

# Java

Referências recomendadas: Java Language Specification, Javadoc e Google Java Style Guide como guia secundário.

- MUST respeitar a versão Java do projeto.
- Classes/interfaces: UpperCamelCase.
- Métodos/variáveis: lowerCamelCase.
- Constantes: UPPER_SNAKE_CASE.
- APIs públicas SHOULD utilizar Javadoc quando o contrato não for trivial.
- MUST NOT introduzir APIs de versão superior ao runtime alvo.
- Exceptions SHOULD preservar causa quando encapsuladas.
- Recursos closeable SHOULD usar try-with-resources quando suportado e adequado.

## Sankhya

Se imports ou contexto indicarem Sankhya, não basta aplicar este arquivo. Leia `stacks/java-sankhya/README.md`.

---

<!-- languages/javascript.md -->

# JavaScript

- SHOULD usar ESLint e Prettier conforme configuração do projeto.
- MUST evitar globals acidentais.
- Promises MUST ter tratamento de erro adequado.
- SHOULD preferir módulos e APIs modernas compatíveis com o runtime alvo.
- Entradas externas MUST ser validadas em fronteiras de confiança.

---

<!-- languages/kotlin.md -->

# Kotlin

Fontes primárias: [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html), [KDoc](https://kotlinlang.org/docs/kotlin-doc.html).

## Ferramentas

- SHOULD usar `ktlint` para estilo e `detekt` para análise estática.
- MUST manter a versão de linguagem/JVM alinhada ao runtime alvo.

## Nulabilidade e tipos

- MUST NOT usar `!!` sem justificativa documentada.
- SHOULD preferir `?.`, `?:` e `requireNotNull` com mensagem útil.
- SHOULD preferir `val` a `var`.
- `data class` SHOULD representar dados sem comportamento relevante.
- `sealed class`/`sealed interface` SHOULD modelar estados finitos, permitindo `when` exaustivo.

## Corrotinas

- MUST usar structured concurrency; MUST NOT usar `GlobalScope` em código de produção.
- Funções `suspend` MUST ser canceláveis e respeitar `CoroutineContext`.
- SHOULD declarar o dispatcher como dependência injetável, para permitir teste.
- MUST NOT capturar `CancellationException` sem relançar.

## Erros e API

- SHOULD preferir tipos de retorno explícitos a exceções para falhas esperadas.
- APIs públicas SHOULD ter KDoc quando o contrato não for trivial.
- Interoperabilidade com Java SHOULD anotar nulabilidade nas fronteiras.

---

<!-- languages/oracle-plsql.md -->

# Oracle SQL / PL/SQL

Referências primárias: Oracle Database documentation. Guia complementar: [PL/SQL & SQL Coding Guidelines](https://primus-delphi-group.github.io/PLSQL_SQL-Coding-Guidelines/) — fork comunitário do guia Trivadis, cujo repositório original foi arquivado.

- SHOULD usar `%TYPE` e `%ROWTYPE` para ancoragem quando apropriado.
- MUST tratar exceptions deliberadamente.
- MUST NOT usar `WHEN OTHERS THEN NULL`.
- `WHEN OTHERS` SHOULD relançar ou transformar a exceção preservando diagnóstico.
- SQL dinâmico SHOULD ser usado apenas quando a estrutura realmente for dinâmica.
- Valores em SQL dinâmico MUST usar bind variables quando possível.
- Procedures reutilizáveis SHOULD NOT executar COMMIT/ROLLBACK sem serem responsáveis pelo limite transacional.
- Triggers SHOULD ser curtas e delegar lógica complexa.

---

<!-- languages/php.md -->

# PHP

Fontes primárias: [PSR-1](https://www.php-fig.org/psr/psr-1/), [PSR-4](https://www.php-fig.org/psr/psr-4/), [PSR-12](https://www.php-fig.org/psr/psr-12/), [documentação oficial](https://www.php.net/docs.php).

## Ferramentas

- SHOULD usar PHP_CodeSniffer ou PHP-CS-Fixer com PSR-12.
- SHOULD usar análise estática (PHPStan ou Psalm) com nível crescente.
- MUST usar Composer com autoload PSR-4 e `composer.lock` versionado.

## Linguagem

- MUST usar `declare(strict_types=1)` em código novo.
- SHOULD tipar parâmetros, retornos e propriedades.
- MUST usar comparação estrita (`===`) salvo necessidade explícita de coerção.
- MUST NOT suprimir erros com `@`.
- MUST NOT usar `eval` nem `extract` sobre entrada externa.

## Segurança

- MUST usar PDO ou driver com prepared statements; MUST NOT interpolar variáveis em SQL.
- Saída em HTML MUST ser escapada (`htmlspecialchars` ou escape do template engine).
- Senhas MUST usar `password_hash`/`password_verify`; MUST NOT usar MD5 ou SHA1.
- Upload de arquivo MUST validar tipo, tamanho e destino fora do document root quando possível.
- Sessões SHOULD usar cookies `HttpOnly`, `Secure` e `SameSite`.
- MUST NOT expor `display_errors` em produção.

---

<!-- languages/python.md -->

# Python

Referências: PEP 8, PEP 257 e documentação oficial de typing.

- SHOULD usar formatter/linter automatizado (ex.: Ruff/Black conforme projeto).
- APIs públicas SHOULD possuir type hints quando isso melhora o contrato.
- Docstrings SHOULD documentar comportamento não trivial, parâmetros, retorno e erros relevantes.
- MUST NOT usar mutable default arguments sem intenção explícita.
- SHOULD preferir pathlib para paths em código moderno quando compatível.

---

<!-- languages/rust.md -->

# Rust

- MUST usar rustfmt conforme projeto.
- SHOULD usar Clippy.
- APIs públicas SHOULD ter rustdoc quando não triviais.
- `unsafe` MUST possuir justificativa e invariantes documentados.
- SHOULD preferir tipos que tornem estados inválidos difíceis de representar.

---

<!-- languages/swift.md -->

# Swift

Fontes primárias: [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/), [DocC](https://www.swift.org/documentation/docc/).

## Nomes

- Nomes MUST priorizar clareza no ponto de uso, não brevidade.
- Métodos com efeito colateral SHOULD usar verbo imperativo (`sort()`); sem efeito, forma nominal (`sorted()`).
- SHOULD nomear parâmetros de forma a compor uma frase legível na chamada.

## Segurança e opcionais

- MUST NOT usar force unwrap (`!`) fora de invariante comprovada e comentada.
- SHOULD usar `guard let` para saída antecipada.
- SHOULD preferir `struct` a `class` quando não houver necessidade de identidade ou herança.
- MUST evitar retain cycles com `[weak self]`/`[unowned self]` em closures que capturam `self`.

## Erros e concorrência

- Falhas esperadas SHOULD usar `throws` e `Result`, não códigos de retorno.
- MUST NOT usar `try!` sem invariante garantida.
- Código concorrente SHOULD usar `async/await` e atores em vez de locks manuais.
- SHOULD habilitar checagem de concorrência estrita nos projetos que a suportem.

## Documentação

- APIs públicas SHOULD usar comentários DocC (`///`) descrevendo parâmetros, retorno e erros.

---

<!-- languages/typescript.md -->

# TypeScript

- SHOULD habilitar `strict` em projetos novos.
- SHOULD preferir `unknown` a `any` para valores não confiáveis.
- `any` SHOULD exigir justificativa quando evitável.
- Tipos públicos SHOULD representar o domínio e o contrato, não apenas satisfazer o compilador.
- Runtime validation MUST existir quando dados entram de fronteira externa; TypeScript não substitui validação em runtime.
