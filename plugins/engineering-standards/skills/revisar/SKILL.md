---
description: Revisa código contra o padrão de engenharia — segurança, qualidade, transação, SQL e documentação. Use quando o usuário pedir revisão de código, revisão de PR ou verificação de conformidade com o padrão.
---

# Revisão contra o padrão

Revise apenas o que mudou. Não proponha refatoração ampla sem relação com a alteração.

## Universal

- [ ] Mudança dentro do escopo pedido.
- [ ] Compatibilidade de runtime preservada.
- [ ] Entrada externa validada na fronteira.
- [ ] SQL parametrizado; nenhuma concatenação com entrada.
- [ ] Nenhum segredo no código.
- [ ] Autorização validada no servidor, não só na UI.
- [ ] Erro não é engolido; causa original preservada.
- [ ] Nome revela intenção; função com responsabilidade coerente.
- [ ] Teste proporcional ao risco; bugfix com teste de regressão.
- [ ] Comentário explica porquê, não o quê.
- [ ] Documentação afetada atualizada.

## Sankhya (quando aplicável)

- [ ] Modelo identificado: legado ou Add-on Studio, sem mistura.
- [ ] APIs usadas existem na versão alvo.
- [ ] Entrypoint enxuto, lógica delegada.
- [ ] Sessão Jape aberta manualmente é fechada em `finally`.
- [ ] Limite transacional explícito; sem commit/rollback dentro de transação gerenciada.
- [ ] Nenhum nome de tabela ou campo não confirmado no dicionário.
- [ ] Hook escolhido corresponde ao evento de negócio.
- [ ] Sem chamada lenta ou HTTP síncrona em regra transacional.
- [ ] Log preserva contexto sem expor dado sensível.

Reporte os achados ordenados por severidade. Para cada um: arquivo, linha, o que
está errado e o cenário concreto de falha. Não reporte preferência de estilo como defeito.
