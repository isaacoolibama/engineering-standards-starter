# Backend

- Fronteiras MUST validar entrada.
- Regras de negócio SHOULD ficar fora de controllers/adapters quando houver complexidade relevante.
- Transações SHOULD possuir limites claros.
- Erros SHOULD manter distinção entre erro de domínio, validação, infraestrutura e falha inesperada.
- Integrações externas SHOULD definir timeout, retry e idempotência quando aplicável.
- Operações assíncronas SHOULD ser observáveis.
