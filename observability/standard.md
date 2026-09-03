# Observability

Para sistemas distribuídos, considerar OpenTelemetry.

- Logs SHOULD ser estruturados.
- SHOULD existir correlation/trace ID entre componentes quando aplicável.
- Métricas SHOULD refletir comportamento e saúde do serviço.
- Traces SHOULD ser usados para fluxos distribuídos críticos.
- Logs MUST NOT expor secrets ou dados sensíveis desnecessários.
