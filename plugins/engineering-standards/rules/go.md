---
paths:
  - "**/*.go"
---

# Padrão de Engenharia — go

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
