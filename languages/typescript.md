# TypeScript

- SHOULD habilitar `strict` em projetos novos.
- SHOULD preferir `unknown` a `any` para valores não confiáveis.
- `any` SHOULD exigir justificativa quando evitável.
- Tipos públicos SHOULD representar o domínio e o contrato, não apenas satisfazer o compilador.
- Runtime validation MUST existir quando dados entram de fronteira externa; TypeScript não substitui validação em runtime.
