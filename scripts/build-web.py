#!/usr/bin/env python3
"""Gera o pacote para assistentes web (Claude Project, ChatGPT Project/GPT, Gems).

Os documentos do padrão moram em pastas temáticas, e vários compartilham o mesmo
nome de arquivo — sete `standard.md`, quatro `java.md`. Um knowledge base web
mostra só o nome do arquivo, sem a pasta, então subir os documentos como estão
produz uma lista ambígua. Aqui o caminho vira prefixo do nome.

Duas saídas, porque as plataformas divergem no que aceitam:

- `dist/web/standards/`: um arquivo por documento, nome achatado. Use quando a
  plataforma aceitar dezenas de arquivos.
- `dist/web/bundles/`: documentos concatenados por perfil de trabalho. Use quando
  houver limite baixo de arquivos, ou para subir só o recorte da sua stack.

`dist/claude-rules/` e `plugins/*/rules/` MUST NOT ir para a web: são cópias
derivadas destes mesmos documentos, com frontmatter `paths:` que só o Claude Code
interpreta. Subir os dois conjuntos duplica o padrão dentro do knowledge base.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "web"

# Pastas cujo conteúdo é normativo e vai para a web. Ficam de fora: dist/ e
# plugins/ (derivados), .claude/ (regras locais), scripts/, governance de repo.
PASTAS = [
    "api", "architecture", "backend", "checklists", "data", "delivery",
    "documentation", "frontend", "governance", "languages", "observability",
    "quality", "security", "stacks", "supply-chain", "templates", "testing",
]

# Perfil -> (descrição, prefixos de caminho incluídos, nesta ordem)
BUNDLES = {
    "nucleo": (
        "Regras transversais: valem em qualquer stack.",
        ["governance/", "quality/", "documentation/", "testing/", "security/",
         "architecture/"],
    ),
    "sankhya": (
        "Personalização Sankhya: legado e Add-on Studio, mais Java, PL/SQL e SQL.",
        ["stacks/java-sankhya/", "languages/java.md", "languages/oracle-plsql.md",
         "data/sql.md", "checklists/java-sankhya-review.md"],
    ),
    "backend": (
        "Serviços, APIs, bancos, entrega e observabilidade.",
        ["backend/", "api/", "data/", "delivery/", "observability/",
         "supply-chain/"],
    ),
    "frontend": (
        "Interface web e desktop, com as linguagens que a acompanham.",
        ["frontend/", "languages/typescript.md", "languages/javascript.md"],
    ),
    "linguagens": (
        "Convenções por linguagem.",
        ["languages/"],
    ),
}

LINK_MD = re.compile(r"\[([^\]]+)\]\((?!https?:)([^)]+\.md)(?:#[^)]*)?\)")
FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)


def achatar(rel: str) -> str:
    """`stacks/java-sankhya/jape.md` -> `stacks-java-sankhya-jape.md`."""
    return rel.replace("/", "-")


def resolver(origem: str, alvo: str) -> str:
    """Resolve link relativo contra a pasta do documento de origem."""
    base = Path(origem).parent
    try:
        return str((base / alvo).resolve().relative_to(ROOT))
    except ValueError:
        return alvo.lstrip("./")


def preparar(rel: str) -> str:
    """Remove frontmatter e troca links relativos por referência ao nome achatado.

    Fora do repositório não há árvore de arquivos para o link resolver, e um link
    quebrado no knowledge base é pior que nenhum: sugere um documento que o
    assistente não consegue abrir.
    """
    texto = (ROOT / rel).read_text(encoding="utf-8")
    texto = FRONTMATTER.sub("", texto)
    texto = LINK_MD.sub(
        lambda m: f"{m.group(1)} (ver `{achatar(resolver(rel, m.group(2)))}`)", texto
    )
    return texto.strip()


def sem_h1(texto: str) -> str:
    """Descarta o H1 do núcleo ao embuti-lo num bundle, onde o título já existe."""
    linhas = texto.splitlines()
    if linhas and linhas[0].startswith("# "):
        linhas = linhas[1:]
    return "\n".join(linhas).strip()


def documentos() -> list[str]:
    achados = []
    for pasta in PASTAS:
        achados += [
            str(p.relative_to(ROOT)) for p in sorted((ROOT / pasta).rglob("*.md"))
        ]
    return achados


def limpar(destino: Path) -> None:
    destino.mkdir(parents=True, exist_ok=True)
    for antigo in destino.glob("*.md"):
        antigo.unlink()


def main() -> None:
    docs = documentos()
    nucleo = (ROOT / "dist" / "core.md").read_text(encoding="utf-8").strip()

    standards = OUT / "standards"
    limpar(standards)
    # Prefixo 00 para o núcleo aparecer primeiro em listagens alfabéticas.
    (standards / "00-nucleo.md").write_text(nucleo + "\n", encoding="utf-8")
    for rel in docs:
        conteudo = f"> Origem: `{rel}` — Engineering Standards\n\n{preparar(rel)}\n"
        (standards / achatar(rel)).write_text(conteudo, encoding="utf-8")

    bundles = OUT / "bundles"
    limpar(bundles)
    resumo_bundles = []
    for nome, (descricao, prefixos) in BUNDLES.items():
        incluidos = [d for p in prefixos for d in docs if d.startswith(p)]
        partes = [
            f"# Engineering Standards — {nome}",
            "",
            descricao,
            "",
            "## Núcleo",
            "",
            sem_h1(nucleo),
            "",
        ]
        for rel in incluidos:
            partes += ["---", "", f"<!-- {rel} -->", "", preparar(rel), ""]
        destino = bundles / f"{nome}.md"
        destino.write_text("\n".join(partes), encoding="utf-8")
        resumo_bundles.append((destino.name, len(incluidos), destino.stat().st_size))

    print(f"dist/web/standards/: {len(docs) + 1} arquivos")
    print("dist/web/bundles/:")
    for nome, qtd, tamanho in resumo_bundles:
        print(f"  {nome:18s} {qtd:2d} documentos  {tamanho / 1024:5.1f} KB")


if __name__ == "__main__":
    main()
