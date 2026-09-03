---
paths:
  - "**/*.dart"
---

# Padrão de Engenharia — dart

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
