# Logging e Erros no Sankhya

- Mensagens ao usuário MUST ser claras e orientadas à ação.
- Logs técnicos SHOULD conter contexto suficiente para suporte: operação, identificadores funcionais e causa.
- MUST NOT registrar senhas, tokens ou dados sensíveis desnecessários.
- Exceptions SHOULD manter a causa original (`cause`) ao serem encapsuladas.
- MUST NOT usar catch vazio.
- SHOULD evitar mensagens genéricas como "Erro ao processar" sem contexto diagnóstico adicional em log.

Mensagem de usuário e log técnico são responsabilidades distintas.
