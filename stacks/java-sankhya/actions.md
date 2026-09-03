# Ações Java

## Modelo tradicional

Classes que implementam `AcaoRotinaJava` SHOULD manter `doAction(ContextoAcao)` como camada de entrada.

- MUST validar quantidade/seleção de linhas quando a ação depender disso.
- SHOULD retornar feedback objetivo ao usuário.
- SHOULD delegar lógica complexa.
- MUST tratar falhas sem esconder a causa útil.
- MUST respeitar o modo de controle transacional configurado na ação.

## Add-on Studio

Quando `@ActionButton` estiver disponível:

- SHOULD manter `accessControlled = true` salvo requisito explícito contrário.
- SHOULD usar descrição clara.
- SHOULD evitar lógica pesada no action handler.
- Para telas customizadas, SHOULD preferir UI chamando camada de serviço quando esse for o padrão da plataforma alvo.
