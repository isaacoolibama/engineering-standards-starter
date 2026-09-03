# Engineering Standards — sankhya

Personalização Sankhya: legado e Add-on Studio, mais Java, PL/SQL e SQL.

## Núcleo

Responda sempre em português do Brasil.

Antes de escrever ou alterar código:
1. Identifique linguagem, framework, runtime, banco e as convenções já usadas no projeto.
2. Aplique somente as regras da stack em uso.
3. Não invente API, tabela, campo, biblioteca ou recurso de plataforma. Se não puder confirmar, diga que não confirmou.
4. Preserve o comportamento fora do escopo pedido; não refatore por conta própria.

Segurança (obrigatório):
- Toda entrada externa é não confiável.
- SQL sempre parametrizado, nunca concatenado.
- Nenhum segredo no código-fonte.
- Autorização validada no servidor, nunca apenas na interface.
- Nenhuma falha silenciosa: erro não pode ser engolido.

Qualidade:
- Função com responsabilidade única e nome que revela intenção.
- Teste proporcional ao risco; correção de bug acompanha teste de regressão.
- Comentário explica o porquê, não o quê.
- Mudança pequena, verificável e reversível.
- Documentação afetada é atualizada junto.

Sankhya: identifique primeiro se o projeto é legado (AcaoRotinaJava, Jape, DynamicVO, NativeSql) ou Add-on Studio (@ActionButton, @Service, @Listener). Nunca misture os dois modelos. Nunca cite tabela ou campo sem confirmar no dicionário de dados (TDDTAB/TDDCAM).

---

<!-- stacks/java-sankhya/README.md -->

# Java Sankhya Engineering Standard

Extensão específica para projetos Java executados no ecossistema Sankhya.

**Não aplicar em Java comum.**

## Primeiro passo obrigatório: identificar o modelo do projeto

Antes de propor código, o agente MUST identificar sinais do ambiente:

### Personalização tradicional / legado

Exemplos de sinais:

- `br.com.sankhya.extensions.actionbutton.AcaoRotinaJava`
- `ContextoAcao`
- `QueryExecutor`
- `br.com.sankhya.jape.*`
- `JapeSession`
- `EntityFacade`
- `DynamicVO`
- `NativeSql`
- `br.com.sankhya.modelcore.comercial.Regra`
- JAR implantado por Módulo Java

### SDK / Add-on Studio moderno

Exemplos de sinais:

- `@Service`
- `@Component`
- `@Repository`
- `@JapeEntity`
- `@ActionButton`
- `@Listener`
- `@Callback`
- `@BusinessRule`
- `@Transactional`
- projeto Gradle estruturado em módulos Add-on

MUST NOT misturar APIs modernas em projetos que somente suportam o modelo tradicional.
MUST NOT reescrever uma personalização legada para o modelo moderno sem solicitação explícita e validação de compatibilidade.

## Documentos desta stack

- `compatibility.md`
- `architecture.md`
- `jape.md`
- `actions.md`
- `business-rules.md`
- `transactions.md`
- `native-sql.md`
- `services-modern.md`
- `logging-errors.md`
- `security.md`
- `performance.md`
- `documentation.md`
- `dicionario.md`

## Fonte de verdade

Para entidades/campos/serviços, consultar documentação e metadados oficiais do Sankhya. Não inferir nomes de campos.
Referências estão em `references/sources.yml`.

---

<!-- stacks/java-sankhya/actions.md -->

# Ações Java

## Modelo tradicional

Classes que implementam `AcaoRotinaJava` SHOULD manter `doAction(ContextoAcao)` como camada de entrada.

- MUST validar quantidade/seleção de linhas quando a ação depender disso.
- SHOULD retornar feedback objetivo ao usuário.
- SHOULD delegar lógica complexa.
- MUST tratar falhas sem esconder a causa útil.
- MUST respeitar o modo de controle transacional configurado na ação.

## Add-on Studio

Quando `@ActionButton` estiver disponível:

- SHOULD manter `accessControlled = true` salvo requisito explícito contrário.
- SHOULD usar descrição clara.
- SHOULD evitar lógica pesada no action handler.
- Para telas customizadas, SHOULD preferir UI chamando camada de serviço quando esse for o padrão da plataforma alvo.

---

<!-- stacks/java-sankhya/architecture.md -->

# Arquitetura Java Sankhya

## Regra principal

Entrypoints Sankhya SHOULD orquestrar; regras complexas SHOULD ser delegadas para classes de serviço/domínio quando o tamanho justificar.

Exemplos de entrypoints:

- `AcaoRotinaJava#doAction`
- implementações de `Regra`
- `@ActionButton`
- `@Listener`
- `@Callback`
- `@BusinessRule`
- endpoints `@Service`

Entrypoints SHOULD permanecer pequenos, validando contexto, extraindo dados, chamando serviço e retornando feedback.

Para SDK moderno, DTOs SHOULD separar contratos externos de entidades persistentes.

---

<!-- stacks/java-sankhya/business-rules.md -->

# Regras, Listeners, Callbacks e Business Rules

Escolha o hook pelo evento de negócio, não pela conveniência.

## Tradicional

Implementações de `br.com.sankhya.modelcore.comercial.Regra` MUST considerar que callbacks podem ocorrer dentro da transação principal e em eventos de CRUD/confirmação.

- MUST evitar processamento lento.
- MUST evitar chamadas externas síncronas quando bloquearem transação crítica.
- SHOULD verificar contexto/evento antes de executar lógica cara.

## Add-on Studio moderno

Quando disponível:

- `@BusinessRule`: SHOULD ser reservado para eventos comerciais e fluxos de confirmação/faturamento quando apropriado.
- `@Listener`: SHOULD ser preferido para eventos CRUD quando essa for a API indicada.
- `@Callback`: MAY ser usado quando o evento de negócio exigir callback aplicável àquele documento/fluxo.

Regras MUST ser rápidas e previsíveis. Integrações externas SHOULD ser desacopladas da transação principal.

---

<!-- stacks/java-sankhya/compatibility.md -->

# Compatibilidade Sankhya

- MUST identificar versão/runtime e modelo de extensão antes de usar APIs específicas.
- MUST respeitar a versão Java efetivamente utilizada pelo ambiente.
- MUST NOT introduzir sintaxe ou APIs Java acima do runtime alvo.
- SHOULD preservar o padrão tecnológico já utilizado no módulo existente.
- SHOULD considerar módulos JAR, dependências Sankhya e classloading antes de adicionar bibliotecas externas.
- Bibliotecas de terceiros SHOULD ser adicionadas somente quando necessárias e após análise de conflito/licença/tamanho.

Quando a versão ou API não estiver comprovada, o código SHOULD ser apresentado como dependente de validação, nunca como universalmente compatível.

---

<!-- stacks/java-sankhya/dicionario.md -->

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

## Campo padrão × campo customizado

- `ADICIONAL = 'S'` e campos com prefixo `AD_` são **customizações daquela instalação**.
- Tabelas com prefixo `AD_` são customizadas.
- Tabelas com prefixo de sigla da empresa também são customizadas.

Consequência prática:

- Código que depende de campo customizado MUST declarar essa dependência na documentação da rotina.
- Exemplo publicado ou compartilhado MUST NOT citar campo customizado — ele não existe na instalação de quem for ler.
- Ao propor um campo novo, o agente SHOULD sugerir o prefixo `AD_`, nunca alterar campo padrão.

## Ordem de decisão

1. Confirmar no dicionário.
2. Se não confirmar, perguntar ao usuário.
3. Se não puder perguntar, escrever o código marcando o ponto como não verificado.
4. Nunca inventar.

---

<!-- stacks/java-sankhya/documentation.md -->

# Documentação Java Sankhya

Classes públicas e entrypoints SHOULD possuir Javadoc quando o propósito não for trivial.

Para personalizações, documentar quando aplicável:

- ponto de extensão Sankhya utilizado;
- tela/evento que dispara a rotina;
- entidades/tabelas afetadas;
- parâmetros esperados;
- limites transacionais;
- efeitos colaterais;
- dependências de parâmetros/configurações do ERP;
- versão/API mínima quando relevante.

Exemplo:

```java
/**
 * Processa os registros selecionados pela ação configurada na tela de origem.
 *
 * <p>A rotina participa da transação gerenciada pela ação e delega a
 * regra de negócio para o serviço correspondente.</p>
 *
 * @param contexto contexto fornecido pelo Sankhya para a execução da ação
 * @throws Exception quando a validação ou persistência não puder ser concluída
 */
@Override
public void doAction(ContextoAcao contexto) throws Exception {
    // ...
}
```

Comentários internos devem explicar peculiaridades do Sankhya, e não operações triviais de Java.

---

<!-- stacks/java-sankhya/jape.md -->

# Jape

Jape é o mecanismo preferencial de persistência quando a operação se encaixa nas entidades mapeadas do Sankhya.

- SHOULD preferir Jape para CRUD de entidades mapeadas quando não houver razão técnica para SQL nativo.
- MUST fechar sessões abertas manualmente.
- MUST respeitar a transação já existente do contexto.
- SHOULD evitar abrir sessões desnecessárias em loops.
- DynamicVO MUST ter campos acessados com nomes reais e validados no dicionário/metadados.
- MUST NOT inventar nomes de entidades ou campos.

Operações em massa MAY justificar estratégia diferente após avaliação de performance e efeitos de regras/eventos.

---

<!-- stacks/java-sankhya/logging-errors.md -->

# Logging e Erros no Sankhya

- Mensagens ao usuário MUST ser claras e orientadas à ação.
- Logs técnicos SHOULD conter contexto suficiente para suporte: operação, identificadores funcionais e causa.
- MUST NOT registrar senhas, tokens ou dados sensíveis desnecessários.
- Exceptions SHOULD manter a causa original (`cause`) ao serem encapsuladas.
- MUST NOT usar catch vazio.
- SHOULD evitar mensagens genéricas como "Erro ao processar" sem contexto diagnóstico adicional em log.

Mensagem de usuário e log técnico são responsabilidades distintas.

---

<!-- stacks/java-sankhya/native-sql.md -->

# NativeSql / SQL Nativo

SQL nativo é permitido quando Jape não for adequado ou quando houver necessidade de consulta/otimização específica.

- Valores externos MUST ser parametrizados.
- MUST NOT concatenar entrada do usuário diretamente na query.
- SELECT SHOULD listar apenas colunas necessárias.
- Queries críticas SHOULD ser analisadas quanto a índices e plano de execução.
- SQL em loops SHOULD ser revisado para evitar N+1.
- Manipulação direta de tabelas core MUST considerar regras, eventos e integridade que seriam disparados por APIs de negócio.

Antes de UPDATE/DELETE direto em tabelas core, SHOULD confirmar que a operação não depende de lógica interna da plataforma.

---

<!-- stacks/java-sankhya/performance.md -->

# Performance Java Sankhya

Código executado em eventos síncronos do ERP impacta diretamente a experiência do usuário.

- Regras/listeners/callbacks SHOULD executar rapidamente.
- MUST evitar chamadas HTTP síncronas em hooks transacionais críticos quando houver alternativa assíncrona suportada.
- MUST evitar queries repetitivas por linha quando consulta em lote for viável.
- SHOULD buscar somente dados necessários.
- SHOULD medir antes de introduzir cache ou otimização complexa.
- Processamentos longos SHOULD usar mecanismos assíncronos/jobs apropriados ao ambiente.

---

<!-- stacks/java-sankhya/security.md -->

# Segurança Java Sankhya

- MUST respeitar permissões e controles nativos da plataforma.
- Ações modernas SHOULD manter controle de acesso habilitado quando suportado.
- MUST validar parâmetros de ações/serviços no backend.
- MUST usar bind/parametrização em SQL.
- MUST NOT expor credenciais no código-fonte.
- Integrações externas MUST definir armazenamento seguro de credenciais.
- SHOULD aplicar menor privilégio para usuários/conexões de integração.
- MUST NOT confiar que esconder botão/tela constitui autorização.

---

<!-- stacks/java-sankhya/services-modern.md -->

# SDK / Add-on Studio Moderno

Aplicar somente quando o projeto confirmar suporte.

- `@Service` SHOULD atuar como fronteira/orquestração.
- `@Component`/business services SHOULD concentrar lógica reutilizável.
- `@Repository` SHOULD encapsular persistência quando essa arquitetura estiver em uso.
- DTOs SHOULD ser usados em contratos de entrada/saída; entidades persistentes SHOULD NOT ser expostas diretamente sem necessidade.
- `@Transactional` SHOULD delimitar operações atômicas de negócio quando suportado.
- Injeção/abstrações SHOULD ser proporcionais à complexidade; não criar camadas vazias apenas para cumprir desenho arquitetural.

---

<!-- stacks/java-sankhya/transactions.md -->

# Transações no Sankhya

Transação é parte do contrato do entrypoint.

- MUST identificar se o framework controla a transação.
- MUST NOT executar commit/rollback arbitrário dentro de código chamado por transação gerenciada.
- Sessões Jape abertas manualmente MUST ser fechadas em `finally` quando o modelo exigir.
- Em ações configuradas com controle manual, o código MUST assumir explicitamente a responsabilidade transacional.
- No SDK moderno, `@Transactional` SHOULD ser usado somente quando suportado e apropriado ao limite de negócio.
- Exceptions utilizadas para rollback MUST preservar contexto diagnóstico.

Não misturar dois modelos de gerenciamento transacional sem justificativa explícita.

---

<!-- languages/java.md -->

# Java

Referências recomendadas: Java Language Specification, Javadoc e Google Java Style Guide como guia secundário.

- MUST respeitar a versão Java do projeto.
- Classes/interfaces: UpperCamelCase.
- Métodos/variáveis: lowerCamelCase.
- Constantes: UPPER_SNAKE_CASE.
- APIs públicas SHOULD utilizar Javadoc quando o contrato não for trivial.
- MUST NOT introduzir APIs de versão superior ao runtime alvo.
- Exceptions SHOULD preservar causa quando encapsuladas.
- Recursos closeable SHOULD usar try-with-resources quando suportado e adequado.

## Sankhya

Se imports ou contexto indicarem Sankhya, não basta aplicar este arquivo. Leia `stacks/java-sankhya/README.md`.

---

<!-- languages/oracle-plsql.md -->

# Oracle SQL / PL/SQL

Referências primárias: Oracle Database documentation. Guia complementar: [PL/SQL & SQL Coding Guidelines](https://primus-delphi-group.github.io/PLSQL_SQL-Coding-Guidelines/) — fork comunitário do guia Trivadis, cujo repositório original foi arquivado.

- SHOULD usar `%TYPE` e `%ROWTYPE` para ancoragem quando apropriado.
- MUST tratar exceptions deliberadamente.
- MUST NOT usar `WHEN OTHERS THEN NULL`.
- `WHEN OTHERS` SHOULD relançar ou transformar a exceção preservando diagnóstico.
- SQL dinâmico SHOULD ser usado apenas quando a estrutura realmente for dinâmica.
- Valores em SQL dinâmico MUST usar bind variables quando possível.
- Procedures reutilizáveis SHOULD NOT executar COMMIT/ROLLBACK sem serem responsáveis pelo limite transacional.
- Triggers SHOULD ser curtas e delegar lógica complexa.

---

<!-- data/sql.md -->

# SQL

- MUST usar parâmetros/bind variables para valores externos.
- SHOULD selecionar apenas colunas necessárias em código permanente.
- SHOULD usar JOIN explícito.
- MUST usar IS NULL / IS NOT NULL para nulidade.
- SHOULD verificar impacto de índices, cardinalidade e filtros em consultas críticas.
- UPDATE/DELETE MUST possuir predicado deliberadamente validado quando a intenção não for afetar todas as linhas.

---

<!-- checklists/java-sankhya-review.md -->

# Java Sankhya Review Checklist

- [ ] Modelo do projeto identificado: tradicional/legado ou SDK/Add-on Studio.
- [ ] Versão Java/runtime compatível.
- [ ] APIs Sankhya utilizadas existem no alvo.
- [ ] Entry point está enxuto.
- [ ] Jape/session é fechado corretamente quando aberto manualmente.
- [ ] Limite transacional está claro.
- [ ] SQL nativo usa parâmetros.
- [ ] Campos/entidades foram validados; nenhum nome foi inventado.
- [ ] Hook escolhido corresponde ao evento de negócio.
- [ ] Não há chamadas lentas em regra transacional crítica.
- [ ] Feedback ao usuário é adequado.
- [ ] Logs preservam contexto sem expor secrets.
