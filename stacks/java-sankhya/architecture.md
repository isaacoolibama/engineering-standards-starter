# Arquitetura Java Sankhya

## Regra principal

Entrypoints Sankhya SHOULD orquestrar; regras complexas SHOULD ser delegadas para classes de serviço/domínio quando o tamanho justificar.

Exemplos de entrypoints:

- `AcaoRotinaJava#doAction`
- implementações de `Regra`
- `@ActionButton`
- `@Listener`
- `@Callback`
- `@BusinessRule`
- endpoints `@Service`

Entrypoints SHOULD permanecer pequenos, validando contexto, extraindo dados, chamando serviço e retornando feedback.

Para SDK moderno, DTOs SHOULD separar contratos externos de entidades persistentes.
