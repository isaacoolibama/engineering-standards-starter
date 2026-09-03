# Engineering Standards — nucleo

Regras transversais: valem em qualquer stack.

## Núcleo

Responda sempre em português do Brasil.

Antes de escrever ou alterar código:
1. Identifique linguagem, framework, runtime, banco e as convenções já usadas no projeto.
2. Aplique somente as regras da stack em uso.
3. Não invente API, tabela, campo, biblioteca ou recurso de plataforma. Se não puder confirmar, diga que não confirmou.
4. Preserve o comportamento fora do escopo pedido; não refatore por conta própria.

Segurança (obrigatório):
- Toda entrada externa é não confiável.
- SQL sempre parametrizado, nunca concatenado.
- Nenhum segredo no código-fonte.
- Autorização validada no servidor, nunca apenas na interface.
- Nenhuma falha silenciosa: erro não pode ser engolido.

Qualidade:
- Função com responsabilidade única e nome que revela intenção.
- Teste proporcional ao risco; correção de bug acompanha teste de regressão.
- Comentário explica o porquê, não o quê.
- Mudança pequena, verificável e reversível.
- Documentação afetada é atualizada junto.

Sankhya: identifique primeiro se o projeto é legado (AcaoRotinaJava, Jape, DynamicVO, NativeSql) ou Add-on Studio (@ActionButton, @Service, @Listener). Nunca misture os dois modelos. Nunca cite tabela ou campo sem confirmar no dicionário de dados (TDDTAB/TDDCAM).

---

<!-- governance/exceptions.md -->

# Exceptions

Uma exceção a uma regra SHOULD registrar:

- regra desviada;
- motivo técnico;
- escopo;
- risco;
- mitigação;
- prazo de revisão, quando temporária.

Exceções temporárias SHOULD possuir issue, ticket ou TODO rastreável.

---

<!-- governance/requirement-levels.md -->

# Requirement Levels

Este repositório usa a semântica BCP 14 (RFC 2119 + RFC 8174).

- **MUST / REQUIRED**: requisito obrigatório.
- **MUST NOT**: comportamento proibido.
- **SHOULD / RECOMMENDED**: padrão esperado; exceções exigem justificativa.
- **SHOULD NOT**: normalmente não permitido; exceções exigem justificativa.
- **MAY / OPTIONAL**: decisão contextual.

Evite usar MUST para preferências cosméticas que não tragam impacto técnico mensurável.

---

<!-- governance/standards-hierarchy.md -->

# Standards Hierarchy

## Ordem de precedência

1. Segurança, compliance e requisitos legais aplicáveis.
2. Requisitos explícitos da entrega.
3. Restrições documentadas do projeto e runtime.
4. Especificação oficial da plataforma/framework.
5. Especificação oficial da linguagem.
6. Este Engineering Standard.
7. Guias secundários de mercado.

Quando houver conflito, registrar a decisão quando o impacto for arquitetural ou recorrente.

---

<!-- quality/code-quality.md -->

# Code Quality

Código SHOULD otimizar para legibilidade, correção, manutenibilidade, testabilidade e segurança.

- Funções SHOULD possuir responsabilidade coerente.
- Nomes MUST revelar intenção.
- Duplicação relevante SHOULD ser eliminada quando a abstração resultante for mais simples.
- Complexidade SHOULD ser reduzida quando prejudicar revisão ou teste.
- Otimização de performance SHOULD ser baseada em evidência quando não for óbvia.

---

<!-- documentation/api-docs.md -->

# API Documentation

APIs públicas SHOULD possuir contrato legível por máquina quando houver padrão adequado.

- HTTP: OpenAPI.
- Eventos/mensageria: AsyncAPI.
- Estruturas JSON: JSON Schema.
- gRPC: Protocol Buffers como contrato primário.

Documentação MUST refletir o comportamento publicado e SHOULD ser validada no CI.

---

<!-- documentation/code-comments.md -->

# Code Comments

Comentários devem responder preferencialmente **por quê?** e não **o quê?**.

## MUST documentar quando relevante

- regra de negócio não óbvia;
- workaround;
- limitação de plataforma;
- comportamento contraintuitivo;
- risco de concorrência/transação;
- requisito de compatibilidade;
- formato/protocolo não autoexplicativo.

## MUST NOT

```java
// Incrementa contador
contador++;
```

## Preferível

```java
// Incrementa antes da persistência porque a sequência é calculada
// a partir do valor corrente na mesma transação.
contador++;
```

Código morto não deve permanecer comentado; use controle de versão.

---

<!-- documentation/standard.md -->

# Documentation Standard

## Modelo Diátaxis

Documentação SHOULD ser classificada em:

- Tutorial: aprendizagem guiada.
- How-to: resolução de tarefa concreta.
- Reference: descrição precisa de contratos e interfaces.
- Explanation: contexto, conceitos e decisões.

Não misturar todos os objetivos em um único documento quando a separação melhorar navegação e manutenção.

## Artefatos mínimos por projeto

Conforme porte e risco:

- README.md
- ARCHITECTURE.md ou docs/architecture/
- SECURITY.md quando aplicável
- documentação de API/contratos
- documentação de configuração e deploy
- troubleshooting operacional
- ADRs para decisões arquiteturais relevantes

---

<!-- testing/standard.md -->

# Testing

Teste deve ser proporcional ao risco.

- Unit: lógica isolada.
- Integration: banco, filesystem, filas, serviços, framework.
- Contract: APIs e integrações.
- E2E: jornadas críticas.
- Security/performance: quando o risco exigir.

Bugfixes SHOULD adicionar teste de regressão quando economicamente viável.
Tests MUST ser determinísticos ou explicitar dependências externas.

---

<!-- security/secrets.md -->

# Secrets

Secrets incluem senhas, tokens, chaves privadas, credenciais, connection strings sensíveis e material criptográfico.

- MUST NOT ser commitados.
- MUST ser fornecidos por mecanismo seguro de configuração/secret store.
- SHOULD possuir rotação.
- SHOULD ser separados por ambiente.
- Logs MUST NOT registrar secrets completos.

---

<!-- security/secure-development.md -->

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

---

<!-- security/threat-modeling.md -->

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

---

<!-- architecture/adr.md -->

# Architecture Decision Records

Use ADR para decisões difíceis de reverter ou que influenciem múltiplos componentes.

Template recomendado: `templates/ADR.md`.

Um ADR SHOULD conter:

- contexto;
- decisão;
- alternativas;
- consequências positivas;
- consequências negativas;
- status.

---

<!-- architecture/standard.md -->

# Architecture Standard

Arquitetura deve ser proporcional à complexidade.

- MUST documentar limites e dependências relevantes.
- SHOULD usar C4 para comunicação visual quando adequado.
- SHOULD registrar decisões relevantes em ADRs.
- SHOULD documentar restrições, riscos e requisitos de qualidade.
- MUST NOT aplicar microservices, CQRS, DDD ou outras abordagens apenas por preferência.

Para documentação arquitetural extensa, arc42 é uma estrutura recomendada.
