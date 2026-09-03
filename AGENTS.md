# Agent Engineering Contract

Este repositório define padrões de engenharia reutilizáveis.

## Regras de operação

- MUST identificar linguagem, framework, runtime, banco, plataforma e convenções existentes antes de alterar código.
- MUST respeitar compatibilidade do projeto alvo.
- MUST aplicar somente regras pertinentes à stack em uso.
- MUST preservar comportamento fora do escopo solicitado.
- MUST NOT realizar refatorações amplas sem relação direta com a tarefa.
- MUST NOT inventar APIs, tabelas, campos, bibliotecas ou recursos de plataforma.
- SHOULD consultar documentação primária quando uma API, versão ou comportamento for incerto.
- SHOULD preferir mudanças pequenas, verificáveis e reversíveis.
- SHOULD atualizar documentação afetada pela alteração.

## Documentação e comentários

- Comentários MUST explicar intenção, contexto, regra de negócio, restrição ou decisão não óbvia.
- Comentários MUST NOT narrar operações triviais do código.
- APIs públicas SHOULD usar o mecanismo nativo de documentação da linguagem.
- Documentação SHOULD registrar contrato, parâmetros, retornos, erros, efeitos colaterais e limitações quando aplicável.

## Segurança

- MUST tratar toda entrada externa como não confiável.
- MUST NOT hardcode secrets.
- MUST usar queries parametrizadas/bind variables quando houver entrada de dados em SQL.
- MUST aplicar princípio do menor privilégio.
- MUST NOT ocultar falhas silenciosamente.

## Qualidade

- MUST manter responsabilidade clara de funções/métodos.
- SHOULD evitar complexidade acidental e abstrações prematuras.
- SHOULD adicionar ou atualizar testes compatíveis com o risco da alteração.
- SHOULD usar linters, formatters e analyzers nativos da stack.

## Java Sankhya

Somente quando o projeto for Sankhya, carregar também `stacks/java-sankhya/`.

Antes de gerar código Sankhya, MUST determinar qual modelo é suportado pelo projeto:

1. personalização tradicional/legada; ou
2. SDK/Add-on Studio moderno.

MUST NOT usar anotações, interfaces ou APIs modernas em projeto que não as suporte.

Consulte `stacks/java-sankhya/README.md`.
