---
description: Instala as regras por linguagem deste padrão em ~/.claude/rules/, para que carreguem automaticamente conforme o tipo de arquivo aberto, em todos os projetos da máquina.
disable-model-invocation: true
---

# Instalar as regras por linguagem

O plugin traz as skills, que carregam sob demanda. As regras com `paths:` são um
mecanismo diferente: disparam de forma determinística pelo tipo de arquivo aberto.
Elas não são instaladas pelo plugin automaticamente — este comando faz isso.

Execute o script empacotado e depois relate ao usuário o que foi instalado:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/instalar-regras.sh"
```

Em seguida, oriente o usuário a abrir uma sessão nova e rodar `/context` para
confirmar. Regras com `paths:` só aparecem depois que um arquivo do tipo
correspondente é aberto.

Para desinstalar: remova `~/.claude/rules/engineering-standards`.
