#!/usr/bin/env python3
"""Gera regras auto-contidas para ~/.claude/rules/ a partir dos documentos do padrão.

As regras em .claude/rules/ do repositório apontam para caminhos relativos, que só
resolvem dentro do repositório. Para uso global, a regra precisa carregar o conteúdo
em si — é o que este script faz.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "claude-rules"

# nome do arquivo -> (globs, [documentos de origem], nota extra)
MAPA = {
    "java": (["**/*.java"], ["languages/java.md"],
             "Se imports ou contexto indicarem Sankhya, aplicar também a regra `sankhya`."),
    "python": (["**/*.py", "**/*.pyi"], ["languages/python.md"], None),
    "typescript": (["**/*.ts", "**/*.tsx"], ["languages/typescript.md", "frontend/react.md"], None),
    "javascript": (["**/*.js", "**/*.jsx", "**/*.mjs", "**/*.cjs"], ["languages/javascript.md"], None),
    "sql": (["**/*.sql", "**/*.pks", "**/*.pkb"], ["data/sql.md", "languages/oracle-plsql.md"], None),
    "go": (["**/*.go"], ["languages/go.md"], None),
    "csharp": (["**/*.cs"], ["languages/csharp.md"], None),
    "kotlin": (["**/*.kt", "**/*.kts"], ["languages/kotlin.md"], None),
    "swift": (["**/*.swift"], ["languages/swift.md"], None),
    "dart": (["**/*.dart"], ["languages/dart.md"], None),
    "php": (["**/*.php"], ["languages/php.md"], None),
    "cpp": (["**/*.{cpp,cc,cxx,hpp,hh,hxx}"], ["languages/cpp.md"], None),
    "rust": (["**/*.rs"], ["languages/rust.md"], None),
}


def corpo(doc: str) -> str:
    """Remove o título H1 e a linha de fontes, que viram cabeçalho da regra."""
    linhas = (ROOT / doc).read_text(encoding="utf-8").splitlines()
    return "\n".join(l for l in linhas if not l.startswith("# ")).strip()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for antigo in OUT.glob("*.md"):
        antigo.unlink()

    for nome, (globs, docs, nota) in MAPA.items():
        partes = [
            "---",
            "paths:",
            *[f'  - "{g}"' for g in globs],
            "---",
            "",
            f"# Padrão de Engenharia — {nome}",
            "",
        ]
        for doc in docs:
            partes.append(corpo(doc))
            partes.append("")
        if nota:
            partes.append(nota)
            partes.append("")
        (OUT / f"{nome}.md").write_text("\n".join(partes), encoding="utf-8")

    # Regra Sankhya: enxuta e path-scoped. O detalhe completo fica em stacks/,
    # carregado apenas quando se trabalha dentro de um projeto Sankhya.
    partes = [
        "---",
        "paths:",
        '  - "**/*.java"',
        '  - "**/*.sql"',
        "---",
        "",
        "# Padrão de Engenharia — Sankhya",
        "",
        "Aplicar SOMENTE se o projeto for Sankhya. Em Java comum, ignorar esta regra.",
        "",
        "## 1. Identificar o modelo antes de gerar código",
        "",
        "- **Legado**: `AcaoRotinaJava`, `ContextoAcao`, `JapeSession`, `EntityFacade`,",
        "  `DynamicVO`, `NativeSql`, `br.com.sankhya.modelcore.comercial.Regra`, JAR por Módulo Java.",
        "- **Add-on Studio**: `@Service`, `@Component`, `@Repository`, `@JapeEntity`,",
        "  `@ActionButton`, `@Listener`, `@Callback`, `@BusinessRule`, `@Transactional`, projeto Gradle.",
        "",
        "MUST NOT misturar APIs modernas em projeto que só suporta o modelo tradicional.",
        "MUST NOT migrar personalização legada para o modelo moderno sem pedido explícito.",
        "",
        "## 2. Nunca inventar tabela, campo ou entidade",
        "",
        "Antes de citar qualquer nome, confirmar no dicionário de dados:",
        "",
        "```sql",
        "SELECT NOMETAB, NOMECAMPO, TIPCAMPO, TAMANHO, ADICIONAL",
        "  FROM TDDCAM",
        " WHERE NOMETAB = :tabela AND NOMECAMPO = :campo;",
        "```",
        "",
        "Zero linhas significa que o campo não existe. Não tentar um nome parecido.",
        "Sem acesso ao banco, MUST declarar explicitamente que o nome não foi confirmado.",
        "Campos com `ADICIONAL = 'S'` ou prefixo `AD_` são customizações daquela instalação.",
        "",
        "## 3. Transação e performance",
        "",
        "- MUST identificar se o framework controla a transação; MUST NOT dar commit/rollback",
        "  arbitrário dentro de transação gerenciada.",
        "- Sessões Jape abertas manualmente MUST ser fechadas em `finally`.",
        "- SQL nativo MUST ser parametrizado.",
        "- Regras/listeners MUST ser rápidos; MUST NOT fazer chamada HTTP síncrona em hook transacional.",
        "",
    ]
    (OUT / "sankhya.md").write_text("\n".join(partes), encoding="utf-8")

    # Espelha as regras dentro do plugin, para que ele seja auto-suficiente.
    plugin_rules = ROOT / "plugins" / "engineering-standards" / "rules"
    if plugin_rules.parent.exists():
        plugin_rules.mkdir(parents=True, exist_ok=True)
        for antigo in plugin_rules.glob("*.md"):
            antigo.unlink()
        for src in OUT.glob("*.md"):
            (plugin_rules / src.name).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    gerados = sorted(p.name for p in OUT.glob("*.md"))
    print(f"{len(gerados)} regras geradas em dist/claude-rules/:")
    for g in gerados:
        linhas = len((OUT / g).read_text(encoding='utf-8').splitlines())
        print(f"  {g:16s} {linhas:3d} linhas")


if __name__ == "__main__":
    main()
