> Origem: `data/sql.md` — Engineering Standards

# SQL

- MUST usar parâmetros/bind variables para valores externos.
- SHOULD selecionar apenas colunas necessárias em código permanente.
- SHOULD usar JOIN explícito.
- MUST usar IS NULL / IS NOT NULL para nulidade.
- SHOULD verificar impacto de índices, cardinalidade e filtros em consultas críticas.
- UPDATE/DELETE MUST possuir predicado deliberadamente validado quando a intenção não for afetar todas as linhas.
