> Origem: `languages/csharp.md` — Engineering Standards

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
