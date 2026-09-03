# Testing

Teste deve ser proporcional ao risco.

- Unit: lógica isolada.
- Integration: banco, filesystem, filas, serviços, framework.
- Contract: APIs e integrações.
- E2E: jornadas críticas.
- Security/performance: quando o risco exigir.

Bugfixes SHOULD adicionar teste de regressão quando economicamente viável.
Tests MUST ser determinísticos ou explicitar dependências externas.
