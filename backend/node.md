# Node.js

Fonte primária: [documentação oficial da versão LTS alvo](https://nodejs.org/docs/latest/api/).

## Runtime e projeto

- MUST declarar a versão suportada em `engines` e alinhar com o CI.
- SHOULD usar apenas LTS ativa em produção.
- MUST versionar lockfile.
- SHOULD definir o sistema de módulos explicitamente (`"type"` no `package.json`).

## Assíncrono e erros

- MUST tratar rejeição de toda Promise; MUST NOT deixar rejeição não tratada.
- MUST NOT bloquear o event loop com trabalho síncrono pesado — usar worker threads ou processo separado.
- Handlers de `uncaughtException` MUST NOT ser usados para continuar execução normal.
- Erros de domínio SHOULD ser distintos de erros de infraestrutura na fronteira HTTP.

## Segurança

- Entrada externa MUST ser validada em runtime na fronteira (body, query, headers, env).
- MUST NOT construir comandos de shell com entrada externa; usar `execFile` com argumentos.
- Caminhos de arquivo derivados de entrada MUST ser normalizados e confinados (path traversal).
- Segredos MUST vir de variáveis de ambiente ou secret store, nunca do código.
- SHOULD executar auditoria de dependências no CI.

## Operação

- MUST implementar shutdown gracioso: parar de aceitar conexões, drenar e encerrar recursos em `SIGTERM`.
- SHOULD expor health/readiness quando houver orquestrador.
- Logs SHOULD ser estruturados e sem dados sensíveis.
- Chamadas externas MUST ter timeout explícito.
