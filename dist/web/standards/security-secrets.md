> Origem: `security/secrets.md` — Engineering Standards

# Secrets

Secrets incluem senhas, tokens, chaves privadas, credenciais, connection strings sensíveis e material criptográfico.

- MUST NOT ser commitados.
- MUST ser fornecidos por mecanismo seguro de configuração/secret store.
- SHOULD possuir rotação.
- SHOULD ser separados por ambiente.
- Logs MUST NOT registrar secrets completos.
