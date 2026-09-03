# Database Design

- Toda tabela persistente SHOULD possuir chave estável adequada ao domínio.
- Integridade SHOULD ser garantida no banco quando possível: PK, FK, UNIQUE, CHECK, NOT NULL.
- Índices SHOULD existir por necessidade observada, não por reflexo.
- Migrations MUST ser reproduzíveis e versionadas.
- Mudanças destrutivas SHOULD possuir estratégia de rollback/migração.
