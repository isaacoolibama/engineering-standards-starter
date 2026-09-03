> Origem: `stacks/java-sankhya/compatibility.md` — Engineering Standards

# Compatibilidade Sankhya

- MUST identificar versão/runtime e modelo de extensão antes de usar APIs específicas.
- MUST respeitar a versão Java efetivamente utilizada pelo ambiente.
- MUST NOT introduzir sintaxe ou APIs Java acima do runtime alvo.
- SHOULD preservar o padrão tecnológico já utilizado no módulo existente.
- SHOULD considerar módulos JAR, dependências Sankhya e classloading antes de adicionar bibliotecas externas.
- Bibliotecas de terceiros SHOULD ser adicionadas somente quando necessárias e após análise de conflito/licença/tamanho.

Quando a versão ou API não estiver comprovada, o código SHOULD ser apresentado como dependente de validação, nunca como universalmente compatível.
