> Origem: `security/secure-development.md` — Engineering Standards

# Secure Development

Base conceitual recomendada:

- NIST SSDF;
- OWASP ASVS;
- OWASP Cheat Sheet Series;
- OpenSSF;
- SLSA para supply chain.

## Regras universais

- MUST validar entradas em fronteiras de confiança.
- MUST parametrizar comandos SQL.
- MUST proteger secrets fora do código.
- MUST aplicar autorização no servidor, não apenas na UI.
- MUST evitar exposição de stack traces e informações sensíveis.
- SHOULD produzir logs de segurança úteis sem registrar dados secretos.
- SHOULD manter dependências atualizadas e auditáveis.
