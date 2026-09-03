---
description: Padrão de engenharia para o ecossistema Sankhya. Use ao escrever, revisar ou depurar código de personalização Sankhya — Java legado (AcaoRotinaJava, Jape, DynamicVO, NativeSql), Add-on Studio (@ActionButton, @Service, @Listener), PL/SQL do ERP, ou qualquer código que cite tabelas e campos do Sankhya.
---

# Padrão Sankhya

Aplicar SOMENTE quando o projeto for Sankhya. Em Java comum, não usar.

## 1. Identificar o modelo antes de gerar código

Determine qual modelo o projeto suporta. Isso MUST ser feito antes de escrever qualquer linha.

**Legado / personalização tradicional** — sinais:
`br.com.sankhya.extensions.actionbutton.AcaoRotinaJava`, `ContextoAcao`, `JapeSession`,
`EntityFacade`, `DynamicVO`, `NativeSql`, `QueryExecutor`,
`br.com.sankhya.modelcore.comercial.Regra`, JAR publicado por Módulo Java, build Maven.

**SDK / Add-on Studio** — sinais:
`@Service`, `@Component`, `@Repository`, `@JapeEntity`, `@ActionButton`, `@Listener`,
`@Callback`, `@BusinessRule`, `@Transactional`, projeto Gradle em módulos Add-on.

- MUST NOT usar anotações modernas em projeto que só suporta o modelo tradicional.
- MUST NOT migrar personalização legada para o modelo moderno sem pedido explícito.
- Na dúvida, pergunte ao usuário em vez de assumir.

## 2. Nunca inventar tabela, campo ou entidade

Este é o erro mais comum de IA no Sankhya. Antes de citar qualquer nome, use a skill
`verificar-dicionario` ou execute a verificação diretamente.

Sem acesso ao banco, MUST declarar explicitamente que o nome não foi confirmado.
MUST NOT escrever o nome mais plausível como se fosse certo.

## 3. Transação

- MUST identificar se o framework controla a transação.
- MUST NOT executar commit/rollback arbitrário dentro de transação gerenciada.
- Sessões Jape abertas manualmente MUST ser fechadas em `finally`.
- Não misturar dois modelos de gerenciamento transacional.

## 4. SQL e performance

- SQL nativo MUST ser parametrizado; MUST NOT concatenar entrada do usuário.
- Regras, listeners e callbacks MUST ser rápidos.
- MUST NOT fazer chamada HTTP síncrona dentro de hook transacional crítico.
- Manipulação direta de tabela core MUST considerar regras e eventos que seriam
  disparados pelas APIs de negócio.

## 5. Compatibilidade

- MUST respeitar a versão Java do ambiente; MUST NOT usar sintaxe ou API acima dela.
- Quando a versão ou API não for comprovada, apresente o código como dependente de
  validação, nunca como universalmente compatível.

Detalhamento completo por tópico: `${CLAUDE_PLUGIN_ROOT}/rules/sankhya.md`.
