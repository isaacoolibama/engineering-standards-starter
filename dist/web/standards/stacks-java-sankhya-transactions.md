> Origem: `stacks/java-sankhya/transactions.md` — Engineering Standards

# Transações no Sankhya

Transação é parte do contrato do entrypoint.

- MUST identificar se o framework controla a transação.
- MUST NOT executar commit/rollback arbitrário dentro de código chamado por transação gerenciada.
- Sessões Jape abertas manualmente MUST ser fechadas em `finally` quando o modelo exigir.
- Em ações configuradas com controle manual, o código MUST assumir explicitamente a responsabilidade transacional.
- No SDK moderno, `@Transactional` SHOULD ser usado somente quando suportado e apropriado ao limite de negócio.
- Exceptions utilizadas para rollback MUST preservar contexto diagnóstico.

Não misturar dois modelos de gerenciamento transacional sem justificativa explícita.
