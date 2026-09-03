# PostgreSQL

Fonte primária: [documentação oficial da versão alvo](https://www.postgresql.org/docs/).

## Esquema

- MUST declarar a versão alvo; recursos MUST existir nela.
- SHOULD usar `text` em vez de `varchar(n)` quando não houver limite de domínio real.
- SHOULD usar `timestamptz` para instantes; `timestamp` sem timezone SHOULD ser exceção justificada.
- SHOULD usar `numeric` para valores monetários; MUST NOT usar `float`/`double` para dinheiro.
- Chaves naturais SHOULD ser preservadas com `UNIQUE` mesmo quando houver chave sintética.
- SHOULD usar `jsonb` (não `json`) quando houver consulta sobre o conteúdo.

## Consultas e índices

- MUST parametrizar valores externos.
- SHOULD analisar `EXPLAIN (ANALYZE, BUFFERS)` em consultas críticas.
- Índices SHOULD nascer de necessidade medida; índice não usado é custo de escrita.
- SHOULD considerar índice parcial e composto na ordem correta de seletividade.
- SHOULD usar `ON CONFLICT` em vez de leitura seguida de escrita não atômica.

## Transações e concorrência

- MUST manter transações curtas; MUST NOT manter transação aberta durante I/O externo.
- SHOULD definir ordem consistente de acesso para evitar deadlock.
- `SELECT ... FOR UPDATE` SHOULD ser usado quando houver leitura seguida de atualização condicional.
- SHOULD configurar `statement_timeout` e `idle_in_transaction_session_timeout`.

## Migrations e operação

- Migrations MUST ser versionadas, idempotentes quando possível e reversíveis ou com plano de rollback.
- `CREATE INDEX CONCURRENTLY` SHOULD ser usado em tabela grande em produção.
- Alterações bloqueantes (`ALTER TABLE` com rewrite) MUST ser avaliadas quanto a lock.
- Backups MUST ser testados por restauração, não apenas gerados.
