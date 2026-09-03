---
paths:
  - "**/*.java"
  - "**/*.sql"
---

# Padrão de Engenharia — Sankhya

Aplicar SOMENTE se o projeto for Sankhya. Em Java comum, ignorar esta regra.

## 1. Identificar o modelo antes de gerar código

- **Legado**: `AcaoRotinaJava`, `ContextoAcao`, `JapeSession`, `EntityFacade`,
  `DynamicVO`, `NativeSql`, `br.com.sankhya.modelcore.comercial.Regra`, JAR por Módulo Java.
- **Add-on Studio**: `@Service`, `@Component`, `@Repository`, `@JapeEntity`,
  `@ActionButton`, `@Listener`, `@Callback`, `@BusinessRule`, `@Transactional`, projeto Gradle.

MUST NOT misturar APIs modernas em projeto que só suporta o modelo tradicional.
MUST NOT migrar personalização legada para o modelo moderno sem pedido explícito.

## 2. Nunca inventar tabela, campo ou entidade

Antes de citar qualquer nome, confirmar no dicionário de dados:

```sql
SELECT NOMETAB, NOMECAMPO, TIPCAMPO, TAMANHO, ADICIONAL
  FROM TDDCAM
 WHERE NOMETAB = :tabela AND NOMECAMPO = :campo;
```

Zero linhas significa que o campo não existe. Não tentar um nome parecido.
Sem acesso ao banco, MUST declarar explicitamente que o nome não foi confirmado.
Campos com `ADICIONAL = 'S'` ou prefixo `AD_` são customizações daquela instalação.

## 3. Transação e performance

- MUST identificar se o framework controla a transação; MUST NOT dar commit/rollback
  arbitrário dentro de transação gerenciada.
- Sessões Jape abertas manualmente MUST ser fechadas em `finally`.
- SQL nativo MUST ser parametrizado.
- Regras/listeners MUST ser rápidos; MUST NOT fazer chamada HTTP síncrona em hook transacional.
