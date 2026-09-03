> Origem: `stacks/java-sankhya/business-rules.md` — Engineering Standards

# Regras, Listeners, Callbacks e Business Rules

Escolha o hook pelo evento de negócio, não pela conveniência.

## Tradicional

Implementações de `br.com.sankhya.modelcore.comercial.Regra` MUST considerar que callbacks podem ocorrer dentro da transação principal e em eventos de CRUD/confirmação.

- MUST evitar processamento lento.
- MUST evitar chamadas externas síncronas quando bloquearem transação crítica.
- SHOULD verificar contexto/evento antes de executar lógica cara.

## Add-on Studio moderno

Quando disponível:

- `@BusinessRule`: SHOULD ser reservado para eventos comerciais e fluxos de confirmação/faturamento quando apropriado.
- `@Listener`: SHOULD ser preferido para eventos CRUD quando essa for a API indicada.
- `@Callback`: MAY ser usado quando o evento de negócio exigir callback aplicável àquele documento/fluxo.

Regras MUST ser rápidas e previsíveis. Integrações externas SHOULD ser desacopladas da transação principal.
