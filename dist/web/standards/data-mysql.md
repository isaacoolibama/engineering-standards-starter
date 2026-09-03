> Origem: `data/mysql.md` — Engineering Standards

# MySQL

Fonte primária: [documentação oficial da versão alvo](https://dev.mysql.com/doc/).

## Esquema

- MUST usar engine InnoDB.
- MUST usar charset `utf8mb4` com collation adequada; `utf8` (3 bytes) MUST NOT ser usado.
- SHOULD usar `DECIMAL` para valores monetários.
- SHOULD usar `DATETIME` ou `TIMESTAMP` com política de timezone explícita e documentada.
- Chave primária SHOULD ser pequena e crescente, por causa do índice clusterizado.
- MUST declarar `NOT NULL` sempre que o domínio exigir.

## Consultas

- MUST parametrizar valores externos.
- SHOULD verificar plano com `EXPLAIN`/`EXPLAIN ANALYZE`.
- MUST NOT usar `SELECT *` em código permanente.
- SHOULD evitar função sobre coluna indexada no `WHERE` (impede uso do índice).
- SHOULD atentar a conversão implícita de tipo, que invalida índice.

## Modo e transações

- MUST usar `STRICT_TRANS_TABLES`; modo permissivo mascara perda de dados.
- SHOULD definir nível de isolamento de forma consciente (padrão é `REPEATABLE READ`).
- Transações MUST ser curtas e não conter I/O externo.
- DDL MUST ser avaliado quanto a bloqueio; MySQL não tem DDL transacional.
