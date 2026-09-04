> Origem: `stacks/java-sankhya/dicionario.md` — Engineering Standards

# Dicionário de dados — protocolo de verificação

Regra central desta stack: **nenhum nome de tabela, campo ou entidade pode ser escrito sem confirmação no dicionário.** Este documento diz *como* confirmar.

O dicionário do Sankhya vive no próprio banco:

| Tabela | Conteúdo |
|---|---|
| `TDDTAB` | catálogo de tabelas — `NOMETAB`, `DESCRTAB`, `TIPONUMERACAO` |
| `TDDCAM` | catálogo de campos — `NOMETAB`, `NOMECAMPO`, `DESCRCAMPO`, `TIPCAMPO`, `TAMANHO`, `CALCULADO`, `ADICIONAL` |
| `TDDLIG` | ligações entre instâncias — `NUINSTORIG`, `NUINSTDEST`, `TIPLIGACAO`, `NOMELIGACAO` |
| `TDDINS` | instâncias/entidades |
| `TDDOPC` | opções de campos de domínio |

*Estrutura verificada em instalação Sankhya sobre Oracle 19c.*

## Antes de gerar código

O agente MUST executar a verificação abaixo para cada tabela e campo que pretende citar. Se não tiver acesso ao banco, MUST declarar explicitamente que o nome não foi confirmado — MUST NOT apresentar como certo.

### O campo existe?

```sql
SELECT NOMETAB, NOMECAMPO, DESCRCAMPO, TIPCAMPO, TAMANHO, CALCULADO, ADICIONAL
  FROM TDDCAM
 WHERE NOMETAB  = :tabela
   AND NOMECAMPO = :campo;
```

Zero linhas significa que o campo **não existe** naquela instalação. Não tente um nome parecido.

### Quais campos a tabela tem?

```sql
SELECT NOMECAMPO, DESCRCAMPO, TIPCAMPO, TAMANHO
  FROM TDDCAM
 WHERE NOMETAB = :tabela
 ORDER BY ORDEM, NOMECAMPO;
```

### A tabela existe e é padrão?

```sql
SELECT NOMETAB, DESCRTAB, TIPONUMERACAO
  FROM TDDTAB
 WHERE NOMETAB = :tabela;
```

### Quais ligações a entidade tem?

```sql
SELECT NOMELIGACAO, TIPLIGACAO, NUINSTORIG, NUINSTDEST, OBRIGATORIA
  FROM TDDLIG
 WHERE NUINSTORIG = :instancia
    OR NUINSTDEST = :instancia;
```

## Quando não há banco para consultar

Assistente web não abre conexão com o ERP. Para esses casos o dicionário pode ser
exportado do banco e anexado ao contexto como arquivo — `scripts/build-dicionario.py`
gera o pacote, e `INSTALL.md` descreve o procedimento.

O pacote exportado substitui a consulta ao banco apenas para os campos que ele contém.
Ele cobre o produto; customizações da instalação ficam de fora por decisão de
confidencialidade. Campo ausente do pacote MUST ser tratado como não confirmado, não
como inexistente — a regra da ordem de decisão abaixo continua valendo.

## Campo padrão × campo customizado

- `ADICIONAL = 'S'` e campos com prefixo `AD_` são **customizações daquela instalação**.
- Tabelas com prefixo `AD_` são customizadas.
- Tabelas com prefixo de sigla da empresa também são customizadas.
- **Campo** com a sigla da empresa no nome também é customizado, mesmo dentro de tabela
  padrão e mesmo sem `AD_` — `TGFCAB.<SIGLA>CODEMPAUT`, `TGFCAB_<SIGLA>`. Nesse caso
  `ADICIONAL` pode vir `'N'`, e só o nome denuncia a origem.

Consequência prática:

- Código que depende de campo customizado MUST declarar essa dependência na documentação da rotina.
- Exemplo publicado ou compartilhado MUST NOT citar campo customizado — ele não existe na instalação de quem for ler.
- Ao propor um campo novo, o agente SHOULD sugerir o prefixo `AD_`, nunca alterar campo padrão.

## Ordem de decisão

1. Confirmar no dicionário.
2. Se não confirmar, perguntar ao usuário.
3. Se não puder perguntar, escrever o código marcando o ponto como não verificado.
4. Nunca inventar.
