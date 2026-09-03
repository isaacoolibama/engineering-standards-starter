> Origem: `security/threat-modeling.md` — Engineering Standards

# Threat Modeling

Fontes: [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling), [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final).

Sistemas com risco relevante SHOULD ser modelados antes da implementação, não depois do incidente.

## Quatro perguntas

1. O que estamos construindo? (ativos, componentes, fluxos de dados)
2. O que pode dar errado? (ameaças)
3. O que vamos fazer? (controles)
4. Ficou bom? (verificação e risco residual)

## Escopo mínimo

- MUST identificar ativos: dados pessoais, financeiros, credenciais, chaves, dados fiscais.
- MUST identificar fronteiras de confiança: internet/aplicação, aplicação/banco, sistema/integração externa, usuário/administrador.
- SHOULD usar STRIDE como checklist: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege.
- Cada ameaça relevante MUST ter decisão registrada: mitigar, transferir, aceitar ou eliminar.
- Risco aceito MUST ser explícito e ter responsável, conforme exceptions.md (ver `governance-exceptions.md`).

## Quando refazer

- SHOULD ser revisado quando entrar nova integração externa, nova fronteira de rede, novo tipo de dado sensível ou mudança de modelo de autenticação.

## Integrações de ERP

Integrações que trafegam dados fiscais, financeiros ou de parceiros MUST modelar: onde a credencial fica, quem pode acionar a rotina, o que é registrado em log e o que acontece em falha parcial.
