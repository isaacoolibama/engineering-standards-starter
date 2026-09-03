---
paths:
  - "**/*.java"
---

# Padrão de Engenharia — java

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

Se imports ou contexto indicarem Sankhya, aplicar também a regra `sankhya`.
