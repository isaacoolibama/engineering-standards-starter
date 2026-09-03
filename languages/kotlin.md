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
