> Origem: `stacks/java-sankhya/documentation.md` — Engineering Standards

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
