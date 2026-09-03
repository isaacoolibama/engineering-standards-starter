---
paths:
  - "**/*.sql"
  - "**/*.pks"
  - "**/*.pkb"
---

# Padrão de Engenharia — sql

- MUST usar parâmetros/bind variables para valores externos.
- SHOULD selecionar apenas colunas necessárias em código permanente.
- SHOULD usar JOIN explícito.
- MUST usar IS NULL / IS NOT NULL para nulidade.
- SHOULD verificar impacto de índices, cardinalidade e filtros em consultas críticas.
- UPDATE/DELETE MUST possuir predicado deliberadamente validado quando a intenção não for afetar todas as linhas.

Referências primárias: Oracle Database documentation. Guia complementar: [PL/SQL & SQL Coding Guidelines](https://primus-delphi-group.github.io/PLSQL_SQL-Coding-Guidelines/) — fork comunitário do guia Trivadis, cujo repositório original foi arquivado.

- SHOULD usar `%TYPE` e `%ROWTYPE` para ancoragem quando apropriado.
- MUST tratar exceptions deliberadamente.
- MUST NOT usar `WHEN OTHERS THEN NULL`.
- `WHEN OTHERS` SHOULD relançar ou transformar a exceção preservando diagnóstico.
- SQL dinâmico SHOULD ser usado apenas quando a estrutura realmente for dinâmica.
- Valores em SQL dinâmico MUST usar bind variables quando possível.
- Procedures reutilizáveis SHOULD NOT executar COMMIT/ROLLBACK sem serem responsáveis pelo limite transacional.
- Triggers SHOULD ser curtas e delegar lógica complexa.
