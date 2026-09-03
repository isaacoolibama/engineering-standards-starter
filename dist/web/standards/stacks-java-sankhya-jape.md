> Origem: `stacks/java-sankhya/jape.md` — Engineering Standards

# Jape

Jape é o mecanismo preferencial de persistência quando a operação se encaixa nas entidades mapeadas do Sankhya.

- SHOULD preferir Jape para CRUD de entidades mapeadas quando não houver razão técnica para SQL nativo.
- MUST fechar sessões abertas manualmente.
- MUST respeitar a transação já existente do contexto.
- SHOULD evitar abrir sessões desnecessárias em loops.
- DynamicVO MUST ter campos acessados com nomes reais e validados no dicionário/metadados.
- MUST NOT inventar nomes de entidades ou campos.

Operações em massa MAY justificar estratégia diferente após avaliação de performance e efeitos de regras/eventos.
