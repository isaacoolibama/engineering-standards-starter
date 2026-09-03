# React

- Components e Hooks MUST permanecer puros durante renderização.
- Props e state MUST ser tratados como imutáveis.
- Hooks MUST ser chamados no top-level de componentes/hooks.
- Side effects SHOULD ocorrer em mecanismos apropriados, não durante render.
- useEffect SHOULD NOT ser usado para estado derivável sem necessidade externa.
- Componentes SHOULD manter responsabilidade coerente.
