# SDK / Add-on Studio Moderno

Aplicar somente quando o projeto confirmar suporte.

- `@Service` SHOULD atuar como fronteira/orquestração.
- `@Component`/business services SHOULD concentrar lógica reutilizável.
- `@Repository` SHOULD encapsular persistência quando essa arquitetura estiver em uso.
- DTOs SHOULD ser usados em contratos de entrada/saída; entidades persistentes SHOULD NOT ser expostas diretamente sem necessidade.
- `@Transactional` SHOULD delimitar operações atômicas de negócio quando suportado.
- Injeção/abstrações SHOULD ser proporcionais à complexidade; não criar camadas vazias apenas para cumprir desenho arquitetural.
