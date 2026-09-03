---
description: Confirma se uma tabela ou campo existe de fato no dicionário de dados do Sankhya antes de gerar código que os cite. Use sempre que for escrever SQL, Jape, DynamicVO ou qualquer código Sankhya que referencie nome de tabela, campo ou entidade.
---

# Verificar dicionário de dados do Sankhya

Objetivo: impedir que nomes inventados entrem no código. Zero linhas de retorno
significa que **o objeto não existe naquela instalação** — não tente um nome parecido.

## O campo existe?

```sql
SELECT NOMETAB, NOMECAMPO, DESCRCAMPO, TIPCAMPO, TAMANHO, CALCULADO, ADICIONAL
  FROM TDDCAM
 WHERE NOMETAB   = :tabela
   AND NOMECAMPO = :campo;
```

## Quais campos a tabela tem?

```sql
SELECT NOMECAMPO, DESCRCAMPO, TIPCAMPO, TAMANHO
  FROM TDDCAM
 WHERE NOMETAB = :tabela
 ORDER BY ORDEM, NOMECAMPO;
```

## A tabela existe?

```sql
SELECT NOMETAB, DESCRTAB, TIPONUMERACAO
  FROM TDDTAB
 WHERE NOMETAB = :tabela;
```

## Quais ligações a entidade tem?

```sql
SELECT NOMELIGACAO, TIPLIGACAO, NUINSTORIG, NUINSTDEST, OBRIGATORIA
  FROM TDDLIG
 WHERE NUINSTORIG = :instancia
    OR NUINSTDEST = :instancia;
```

## Como interpretar o resultado

- `ADICIONAL = 'S'` ou prefixo `AD_`: campo **customizado daquela instalação**.
  Código que dependa dele MUST declarar essa dependência na documentação da rotina.
  Exemplo compartilhado publicamente MUST NOT citar campo customizado.
- `CALCULADO = 'S'`: campo calculado, não persistido como coluna comum.

## Procedimento

1. Use a conexão de banco já configurada no projeto. Não peça credencial que já exista.
2. Se não houver acesso ao banco, pergunte ao usuário.
3. Se não puder perguntar, escreva o código marcando explicitamente cada nome não
   confirmado como pendente de validação.
4. Nunca invente.
