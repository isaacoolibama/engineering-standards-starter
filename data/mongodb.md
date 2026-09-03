# MongoDB

Fonte primária: [documentação oficial](https://www.mongodb.com/docs/manual/).

## Modelagem

- Modelagem MUST partir dos padrões de acesso, não da normalização relacional.
- SHOULD embutir dados lidos junto; SHOULD referenciar dados grandes, voláteis ou compartilhados.
- Documentos MUST respeitar o limite de 16 MB; arrays MUST ter crescimento limitado.
- SHOULD aplicar JSON Schema validation nas coleções relevantes.

## Consultas e índices

- Toda consulta recorrente MUST ter índice de suporte.
- Índices compostos MUST seguir a ordem igualdade → ordenação → intervalo.
- SHOULD verificar planos com `explain("executionStats")`.
- MUST NOT construir filtros por concatenação de string a partir de entrada externa (injeção de operador).
- Entrada externa MUST ser validada; campos iniciados por `$` MUST ser rejeitados quando não esperados.

## Consistência e operação

- Escritas críticas SHOULD usar `writeConcern` majoritário.
- Transações multi-documento MAY ser usadas quando necessárias, cientes do custo.
- MUST habilitar autenticação e autorização; MUST NOT expor instância sem controle de acesso.
- Conexões SHOULD usar TLS.
