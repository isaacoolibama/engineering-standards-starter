# Padrão de Engenharia — Núcleo

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
