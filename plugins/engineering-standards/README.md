# engineering-standards

Plugin do Claude Code com o padrão de engenharia para desenvolvimento, segurança,
banco de dados e documentação, incluindo o ecossistema Sankhya.

## Instalar

```
/plugin marketplace add isaacoolibama/engineering-standards-starter
/plugin install engineering-standards@engineering-standards
```

## Skills

| Skill | Quando dispara |
|---|---|
| `sankhya` | ao trabalhar com personalização Sankhya |
| `verificar-dicionario` | antes de citar tabela ou campo do Sankhya |
| `revisar` | ao pedir revisão de código contra o padrão |
| `instalar-regras` | manual — instala as regras por linguagem em `~/.claude/rules/` |

## Depois de instalar

As skills carregam sob demanda. Para ter também as regras determinísticas por tipo
de arquivo (Java, Python, Go, SQL, etc.), rode uma vez:

```
/engineering-standards:instalar-regras
```

Confirme com `/context` em uma sessão nova.
