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
