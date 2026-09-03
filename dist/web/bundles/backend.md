# Engineering Standards — backend

Serviços, APIs, bancos, entrega e observabilidade.

## Núcleo

Responda sempre em português do Brasil.

Antes de escrever ou alterar código:
1. Identifique linguagem, framework, runtime, banco e as convenções já usadas no projeto.
2. Aplique somente as regras da stack em uso.
3. Não invente API, tabela, campo, biblioteca ou recurso de plataforma. Se não puder confirmar, diga que não confirmou.
4. Preserve o comportamento fora do escopo pedido; não refatore por conta própria.

Segurança (obrigatório):
- Toda entrada externa é não confiável.
- SQL sempre parametrizado, nunca concatenado.
- Nenhum segredo no código-fonte.
- Autorização validada no servidor, nunca apenas na interface.
- Nenhuma falha silenciosa: erro não pode ser engolido.

Qualidade:
- Função com responsabilidade única e nome que revela intenção.
- Teste proporcional ao risco; correção de bug acompanha teste de regressão.
- Comentário explica o porquê, não o quê.
- Mudança pequena, verificável e reversível.
- Documentação afetada é atualizada junto.

Sankhya: identifique primeiro se o projeto é legado (AcaoRotinaJava, Jape, DynamicVO, NativeSql) ou Add-on Studio (@ActionButton, @Service, @Listener). Nunca misture os dois modelos. Nunca cite tabela ou campo sem confirmar no dicionário de dados (TDDTAB/TDDCAM).

---

<!-- backend/node.md -->

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

---

<!-- backend/standard.md -->

# Backend

- Fronteiras MUST validar entrada.
- Regras de negócio SHOULD ficar fora de controllers/adapters quando houver complexidade relevante.
- Transações SHOULD possuir limites claros.
- Erros SHOULD manter distinção entre erro de domínio, validação, infraestrutura e falha inesperada.
- Integrações externas SHOULD definir timeout, retry e idempotência quando aplicável.
- Operações assíncronas SHOULD ser observáveis.

---

<!-- api/rest.md -->

# REST / HTTP API

- SHOULD usar OpenAPI como contrato.
- MUST utilizar semântica HTTP corretamente.
- SHOULD manter formato de erro consistente.
- SHOULD documentar paginação, filtros, ordenação e idempotência.
- MUST validar autenticação/autorização no backend.
- SHOULD planejar compatibilidade e versionamento antes de breaking changes.

---

<!-- data/database-design.md -->

# Database Design

- Toda tabela persistente SHOULD possuir chave estável adequada ao domínio.
- Integridade SHOULD ser garantida no banco quando possível: PK, FK, UNIQUE, CHECK, NOT NULL.
- Índices SHOULD existir por necessidade observada, não por reflexo.
- Migrations MUST ser reproduzíveis e versionadas.
- Mudanças destrutivas SHOULD possuir estratégia de rollback/migração.

---

<!-- data/mongodb.md -->

# MongoDB

Fonte primária: [documentação oficial](https://www.mongodb.com/docs/manual/).

## Modelagem

- Modelagem MUST partir dos padrões de acesso, não da normalização relacional.
- SHOULD embutir dados lidos junto; SHOULD referenciar dados grandes, voláteis ou compartilhados.
- Documentos MUST respeitar o limite de 16 MB; arrays MUST ter crescimento limitado.
- SHOULD aplicar JSON Schema validation nas coleções relevantes.

## Consultas e índices

- Toda consulta recorrente MUST ter índice de suporte.
- Índices compostos MUST seguir a ordem igualdade → ordenação → intervalo.
- SHOULD verificar planos com `explain("executionStats")`.
- MUST NOT construir filtros por concatenação de string a partir de entrada externa (injeção de operador).
- Entrada externa MUST ser validada; campos iniciados por `$` MUST ser rejeitados quando não esperados.

## Consistência e operação

- Escritas críticas SHOULD usar `writeConcern` majoritário.
- Transações multi-documento MAY ser usadas quando necessárias, cientes do custo.
- MUST habilitar autenticação e autorização; MUST NOT expor instância sem controle de acesso.
- Conexões SHOULD usar TLS.

---

<!-- data/mysql.md -->

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

---

<!-- data/postgresql.md -->

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

---

<!-- data/redis.md -->

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

---

<!-- data/sql.md -->

# SQL

- MUST usar parâmetros/bind variables para valores externos.
- SHOULD selecionar apenas colunas necessárias em código permanente.
- SHOULD usar JOIN explícito.
- MUST usar IS NULL / IS NOT NULL para nulidade.
- SHOULD verificar impacto de índices, cardinalidade e filtros em consultas críticas.
- UPDATE/DELETE MUST possuir predicado deliberadamente validado quando a intenção não for afetar todas as linhas.

---

<!-- data/sqlserver.md -->

# SQL Server / T-SQL

Fonte primária: [documentação Microsoft da versão alvo](https://learn.microsoft.com/sql/sql-server/).

## Esquema

- SHOULD usar `NVARCHAR` quando houver necessidade de Unicode; escolher `VARCHAR` deliberadamente.
- SHOULD usar `DECIMAL`/`NUMERIC` para valores monetários; `MONEY` SHOULD ser evitado.
- SHOULD usar `DATETIME2` em vez de `DATETIME`.
- MUST definir clustered index adequado; heap SHOULD ser exceção justificada.
- MUST qualificar objetos com schema (`dbo.Tabela`).

## Consultas

- MUST parametrizar valores externos; MUST NOT concatenar SQL dinâmico com entrada.
- SQL dinâmico necessário MUST usar `sp_executesql` com parâmetros.
- SHOULD analisar plano de execução em consultas críticas.
- SHOULD atentar a *parameter sniffing* em procedures com cardinalidade variável.
- MUST NOT usar `NOLOCK` como solução padrão de contenção — ele permite leitura suja.

## Procedures e transações

- Procedures SHOULD iniciar com `SET NOCOUNT ON`.
- MUST tratar erro com `TRY...CATCH` e relançar preservando diagnóstico (`THROW`).
- MUST garantir consistência entre `BEGIN TRAN` e `COMMIT`/`ROLLBACK`, inclusive em erro.
- SHOULD usar `SET XACT_ABORT ON` em procedures transacionais.
- Cursores SHOULD ser evitados quando houver solução baseada em conjunto.

## Sankhya

Instalações Sankhya podem usar SQL Server. Ao escrever SQL para o ERP, MUST confirmar o banco alvo — sintaxe Oracle e T-SQL não são intercambiáveis.

---

<!-- delivery/ci-cd.md -->

# CI/CD

Fontes: [OpenSSF](https://openssf.org/), [SLSA](https://slsa.dev/).

## Pipeline mínimo

Todo projeto SHOULD ter, proporcional ao risco:

1. build reprodutível;
2. lint e formatação;
3. testes automatizados;
4. verificação de segurança (dependências e segredos);
5. geração e publicação de artefato versionado.

- O pipeline MUST falhar de forma visível; MUST NOT ter etapa crítica em modo apenas informativo.
- Build MUST ser reproduzível a partir do repositório, sem passo manual não documentado.
- Dependências MUST vir de lockfile.

## Segurança do pipeline

- Segredos MUST vir do cofre do provedor; MUST NOT ficar em variáveis de texto plano no repositório.
- Ações/plugins de terceiros SHOULD ser fixados por versão imutável.
- Permissões do job MUST seguir menor privilégio.
- Pipelines de PR de fork MUST NOT ter acesso a segredos de produção.
- Scanner de segredos SHOULD rodar em todo push.

## Entrega

- Deploy MUST ser automatizado e repetível.
- Promoção entre ambientes SHOULD usar o mesmo artefato, mudando apenas configuração.
- Toda entrega MUST ter procedimento de rollback conhecido.
- Migrations de banco MUST ter ordem definida em relação ao deploy da aplicação.

---

<!-- delivery/git.md -->

# Git and Delivery

- Commits SHOULD representar mudanças coesas.
- Conventional Commits MAY ser adotado para automação de releases.
- Semantic Versioning SHOULD ser usado quando o produto expõe API/versionamento compatível com SemVer.
- CHANGELOG SHOULD registrar mudanças relevantes ao consumidor, não replicar o log bruto do Git.
- CI SHOULD validar build, testes, lint e verificações de segurança compatíveis com o risco.

---

<!-- observability/standard.md -->

# Observability

Para sistemas distribuídos, considerar OpenTelemetry.

- Logs SHOULD ser estruturados.
- SHOULD existir correlation/trace ID entre componentes quando aplicável.
- Métricas SHOULD refletir comportamento e saúde do serviço.
- Traces SHOULD ser usados para fluxos distribuídos críticos.
- Logs MUST NOT expor secrets ou dados sensíveis desnecessários.

---

<!-- supply-chain/standard.md -->

# Software Supply Chain

Projetos relevantes SHOULD avaliar:

- SBOM (SPDX ou CycloneDX);
- pinning/lockfiles;
- proveniência de build;
- assinatura/verificação de artefatos;
- scanners de dependência;
- atualização automatizada de dependências;
- SLSA conforme risco.
