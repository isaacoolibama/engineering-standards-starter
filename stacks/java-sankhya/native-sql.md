# NativeSql / SQL Nativo

SQL nativo é permitido quando Jape não for adequado ou quando houver necessidade de consulta/otimização específica.

- Valores externos MUST ser parametrizados.
- MUST NOT concatenar entrada do usuário diretamente na query.
- SELECT SHOULD listar apenas colunas necessárias.
- Queries críticas SHOULD ser analisadas quanto a índices e plano de execução.
- SQL em loops SHOULD ser revisado para evitar N+1.
- Manipulação direta de tabelas core MUST considerar regras, eventos e integridade que seriam disparados por APIs de negócio.

Antes de UPDATE/DELETE direto em tabelas core, SHOULD confirmar que a operação não depende de lógica interna da plataforma.
