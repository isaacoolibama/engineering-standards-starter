# Redis

Fonte primária: [documentação oficial](https://redis.io/docs/latest/).

## Papel no sistema

- O papel do Redis (cache, fila, estado, lock, rate limit) MUST ser declarado explicitamente.
- Uso como cache MUST tolerar perda total dos dados sem corromper o sistema.
- Uso como fonte de verdade MUST definir persistência (RDB/AOF) e política de recuperação.

## Chaves e memória

- Chaves SHOULD seguir convenção de namespace (`dominio:entidade:id`).
- Toda chave de cache MUST ter TTL; ausência de TTL MUST ser decisão consciente.
- MUST definir `maxmemory` e política de eviction compatível com o papel.
- MUST NOT usar `KEYS` em produção — usar `SCAN`.
- SHOULD evitar estruturas gigantes em chave única (hot key).

## Correção e segurança

- Operações compostas SHOULD usar transação (`MULTI`) ou script Lua para atomicidade.
- Locks distribuídos MUST ter TTL e liberação segura por token do dono.
- MUST exigir autenticação e MUST NOT expor a instância à internet.
- Comandos administrativos perigosos SHOULD ser renomeados ou desabilitados.
- SHOULD usar TLS quando o tráfego sair do host.
