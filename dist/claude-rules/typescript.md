---
paths:
  - "**/*.ts"
  - "**/*.tsx"
---

# Padrão de Engenharia — typescript

- SHOULD habilitar `strict` em projetos novos.
- SHOULD preferir `unknown` a `any` para valores não confiáveis.
- `any` SHOULD exigir justificativa quando evitável.
- Tipos públicos SHOULD representar o domínio e o contrato, não apenas satisfazer o compilador.
- Runtime validation MUST existir quando dados entram de fronteira externa; TypeScript não substitui validação em runtime.

- Components e Hooks MUST permanecer puros durante renderização.
- Props e state MUST ser tratados como imutáveis.
- Hooks MUST ser chamados no top-level de componentes/hooks.
- Side effects SHOULD ocorrer em mecanismos apropriados, não durante render.
- useEffect SHOULD NOT ser usado para estado derivável sem necessidade externa.
- Componentes SHOULD manter responsabilidade coerente.
