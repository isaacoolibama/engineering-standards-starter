> Origem: `data/sqlserver.md` — Engineering Standards

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
