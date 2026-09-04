#!/usr/bin/env python3
"""Gera o dicionário de dados Sankhya a partir da exportação da instalação.

Motivo de existir: o padrão manda confirmar todo nome de tabela e campo antes de
citá-lo, mas nos assistentes web não há banco para consultar. Este script converte
a exportação de `TDDTAB`/`TDDCAM` num pacote de texto que pode ir para o knowledge
base do Project, tornando a confirmação executável fora do ERP.

A separação entre as duas saídas é de confidencialidade, não de conveniência:

- `dist/web/dicionario/` — apenas o que é do produto. Publicável.
- `dist/local/` — o que é da instalação. Expõe esquema interno, e o `.gitignore`
  o mantém fora do repositório público.

A separação usa dois critérios, porque `CUSTOMIZADO` sozinho não pega tudo: além
dos campos marcados, tabelas inteiras podem ser customizadas pelo prefixo do nome
(`AD_`, ou a sigla da empresa — ver `stacks/java-sankhya/dicionario.md`). O prefixo
não é dedutível do CSV, então a classificação vive em `dist/local/PREFIXOS`, fora do
versionamento, e prefixo desconhecido é tratado como privado até alguém decidir.

Não faz parte de `build-web.py` de propósito: o CSV de entrada é dado de uma
instalação específica, opcional e não versionado; o pacote web precisa continuar
sendo gerado sem ele.
"""
import argparse
import csv
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PADRAO = ROOT / "sankhya-dicionario-instalacao.csv"
OUT_WEB = ROOT / "dist" / "web" / "dicionario"
OUT_LOCAL = ROOT / "dist" / "local"

COLUNAS = [
    "TABELA", "DESCRICAO_TABELA", "TIPO_NUMERACAO", "ORDEM_CAMPO", "CAMPO",
    "DESCRICAO_CAMPO", "TIPO_CAMPO", "TAMANHO", "CALCULADO", "ADICIONAL",
    "CUSTOMIZADO",
]

# Um knowledge base mostra só o nome do arquivo. Prefixo fixo para o assistente
# reconhecer o conjunto sem abrir cada arquivo.
PREFIXO = "sankhya-dicionario"

# Acima disso o arquivo é quebrado em partes. Plataformas web variam no limite de
# upload; 450 KB passa em todas as que o INSTALL.md cobre.
LIMITE_BYTES = 450 * 1024

ARQ_PREFIXOS = OUT_LOCAL / "dicionario-prefixos.conf"

# Regra de `stacks/java-sankhya/dicionario.md`: prefixo `AD_` é customização.
PRIVADOS_INICIAIS = {"AD_"}

# A sigla da empresa costuma aparecer dentro de tabela padrão, em campo que não usa
# `AD_` nem está marcado `ADICIONAL = 'S'` — `TGFCAB.<SIGLA>CODEMPAUT`, `TGFCAB_<SIGLA>`.
# Nesses casos a coluna `CUSTOMIZADO` da exportação não acusa nada, e só o nome
# denuncia. Qualquer tabela ou campo que contenha um marcador vai para o privado.
#
# Vazio de propósito: a sigla é de cada instalação e não pertence a este repositório.
# Declare a sua em `dist/local/dicionario-prefixos.conf` com `marcador SIGLA`.
MARCADORES_INICIAIS: set[str] = set()

# Abaixo disso um prefixo é candidato a customização e entra no aviso de revisão:
# módulo do produto traz dezenas de tabelas, personalização traz uma ou duas.
LIMIAR_SUSPEITO = 5

CONF_CABECALHO = """# Classificação dos prefixos de tabela desta instalação.
#
# `publico`  -> vai para dist/web/dicionario/, que pode ser publicado.
# `privado`  -> vai para dist/local/, que o .gitignore mantém fora do repositório.
# `marcador` -> sigla da empresa: toda tabela ou campo que a contenha vira privado,
#               mesmo dentro de tabela padrão do produto.
#
# Prefixo ausente daqui é tratado como privado, e prefixo com poucas tabelas nasce
# privado — o formato típico de personalização. Promova a `publico` o que você
# confirmar ser módulo do produto. Este arquivo não é versionado: a classificação
# é de cada instalação.
"""

CABECALHO = """> Dicionário de dados Sankhya — gerado de `TDDTAB`/`TDDCAM` por
> `scripts/build-dicionario.py`. Fonte normativa do padrão: veja
> `stacks-java-sankhya-dicionario.md`.

Formato de cada linha: `CAMPO | DESCRIÇÃO | TIPCAMPO | TAMANHO | calc`

- `TIPCAMPO` é o código bruto do `TDDCAM`, sem tradução.
- `TAMANHO` em branco significa que o dicionário não o define.
- `calc` marca campo calculado (`CALCULADO = 'S'`).
- Campos em ordem alfabética dentro de cada tabela.

Campo ausente daqui **não existe** nesta instalação. Não use nome parecido.
"""

CABECALHO_LOCAL = """> **Confidencial — não publicar.** Customizações desta instalação
> (`ADICIONAL = 'S'` ou prefixo `AD_`), geradas por `scripts/build-dicionario.py`.

Estes campos não existem em outra instalação Sankhya. Código que dependa deles MUST
declarar a dependência na documentação da rotina, e exemplo compartilhado MUST NOT
citá-los.

Formato de cada linha: `CAMPO | DESCRIÇÃO | TIPCAMPO | TAMANHO | calc`
"""


def prefixo_de(tabela: str) -> str:
    return tabela[:3].upper()


def carregar_prefixos(
    tabelas: list[str],
) -> tuple[dict[str, str], set[str], list[str]]:
    """Lê a classificação, criando o arquivo na primeira execução.

    Retorna o mapa prefixo -> publico|privado, os marcadores de organização e os
    prefixos que ainda faltam classificar.
    """
    contagem: dict[str, int] = {}
    for tabela in tabelas:
        contagem[prefixo_de(tabela)] = contagem.get(prefixo_de(tabela), 0) + 1

    classificacao: dict[str, str] = {}
    marcadores: set[str] = set()
    if ARQ_PREFIXOS.is_file():
        for numero, linha in enumerate(
            ARQ_PREFIXOS.read_text(encoding="utf-8").splitlines(), 1
        ):
            linha = linha.split("#", 1)[0].strip()
            if not linha:
                continue
            partes = linha.split()
            if len(partes) == 2 and partes[0] == "marcador":
                marcadores.add(partes[1].upper())
                continue
            if len(partes) != 2 or partes[1] not in ("publico", "privado"):
                sys.exit(
                    f"ERRO: {ARQ_PREFIXOS.name}:{numero}: esperado "
                    f"`PREFIXO publico|privado` ou `marcador SIGLA`, veio `{linha}`"
                )
            classificacao[partes[0].upper()] = partes[1]
    else:
        OUT_LOCAL.mkdir(parents=True, exist_ok=True)
        marcadores = set(MARCADORES_INICIAIS)
        linhas = [CONF_CABECALHO]
        linhas += [f"marcador {m}" for m in sorted(marcadores)]
        linhas += ["# marcador SIGLA   <- descomente e troque pela sigla da sua empresa", ""]
        for prefixo, qtd in sorted(contagem.items(), key=lambda i: (-i[1], i[0])):
            suspeito = qtd <= LIMIAR_SUSPEITO
            valor = (
                "privado"
                if prefixo in PRIVADOS_INICIAIS or suspeito
                else "publico"
            )
            nota = f"# {qtd} tabelas"
            if suspeito and prefixo not in PRIVADOS_INICIAIS:
                nota += " — REVISAR"
            linhas.append(f"{prefixo:<6} {valor:<8} {nota}")
            classificacao[prefixo] = valor
        ARQ_PREFIXOS.write_text("\n".join(linhas) + "\n", encoding="utf-8")
        print(f"criado {ARQ_PREFIXOS} — revise antes de publicar o pacote")

    faltando = sorted(p for p in contagem if p not in classificacao)
    return classificacao, marcadores, faltando


def ler(caminho: Path) -> list[dict]:
    if not caminho.is_file():
        sys.exit(
            f"ERRO: exportação não encontrada em {caminho}\n"
            "Gere-a no banco da instalação (query em dist/web/dicionario/"
            f"{PREFIXO}-README.md) ou informe o caminho com --csv."
        )
    with caminho.open(newline="", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        faltando = [c for c in COLUNAS if c not in (leitor.fieldnames or [])]
        if faltando:
            sys.exit(f"ERRO: colunas ausentes em {caminho.name}: {', '.join(faltando)}")
        return list(leitor)


def agrupar(linhas: list[dict]) -> "OrderedDict[str, dict]":
    """Agrupa por tabela preservando a ordem de campo do dicionário."""
    tabelas: OrderedDict[str, dict] = OrderedDict()
    # `ORDEM_CAMPO` vem 0 na maior parte das linhas desta exportação, então não
    # ordena nada de útil. Alfabética por campo é o que serve à pergunta que este
    # pacote responde: "este campo existe nesta tabela?".
    for linha in sorted(linhas, key=lambda r: (r["TABELA"], r["CAMPO"])):
        tabela = tabelas.setdefault(
            linha["TABELA"],
            {
                "descricao": linha["DESCRICAO_TABELA"],
                "numeracao": linha["TIPO_NUMERACAO"],
                "campos": [],
            },
        )
        tabela["campos"].append(linha)
    return tabelas


def render(nome: str, tabela: dict) -> str:
    titulo = f"## {nome}"
    if tabela["descricao"]:
        titulo += f" — {tabela['descricao']}"
    partes = [titulo, ""]
    for campo in tabela["campos"]:
        celulas = [
            campo["CAMPO"],
            campo["DESCRICAO_CAMPO"] or "-",
            campo["TIPO_CAMPO"] or "-",
            campo["TAMANHO"] or "",
        ]
        if campo["CALCULADO"] == "S":
            celulas.append("calc")
        partes.append(" | ".join(celulas).rstrip(" |"))
    partes.append("")
    return "\n".join(partes)


def fatiar(tabelas: "OrderedDict[str, dict]") -> "OrderedDict[str, list[str]]":
    """Um arquivo por prefixo de módulo (3 letras), quebrado quando passa do limite."""
    grupos: OrderedDict[str, list[tuple[str, str]]] = OrderedDict()
    for nome, tabela in tabelas.items():
        grupos.setdefault(nome[:3].upper(), []).append((nome, render(nome, tabela)))

    arquivos: OrderedDict[str, list[str]] = OrderedDict()
    for prefixo in sorted(grupos):
        blocos = grupos[prefixo]
        partes, atual, tamanho = [], [], 0
        for _, bloco in blocos:
            if atual and tamanho + len(bloco.encode()) > LIMITE_BYTES:
                partes.append(atual)
                atual, tamanho = [], 0
            atual.append(bloco)
            tamanho += len(bloco.encode())
        if atual:
            partes.append(atual)
        for i, parte in enumerate(partes, 1):
            sufixo = f"-{i}" if len(partes) > 1 else ""
            arquivos[f"{PREFIXO}-{prefixo}{sufixo}.md"] = parte
    return arquivos


def limpar(destino: Path) -> None:
    destino.mkdir(parents=True, exist_ok=True)
    for antigo in destino.glob(f"{PREFIXO}*.md"):
        antigo.unlink()


def escrever_indice(destino: Path, arquivos: dict, tabelas: OrderedDict) -> None:
    linhas = [
        f"# {PREFIXO} — índice",
        "",
        f"{len(tabelas)} tabelas do produto, {sum(len(t['campos']) for t in tabelas.values())} campos.",
        "",
        CABECALHO,
        "## Arquivos",
        "",
    ]
    for nome, blocos in arquivos.items():
        alvos = [b.splitlines()[0][3:].split(" — ")[0] for b in blocos]
        linhas.append(f"- `{nome}` — {len(blocos)} tabelas ({alvos[0]} … {alvos[-1]})")
    linhas += [
        "",
        "## Como esta exportação é gerada",
        "",
        "Rode no banco da instalação e salve como CSV com cabeçalho. As colunas são o",
        "contrato de entrada de `scripts/build-dicionario.py`; `CUSTOMIZADO` é derivada.",
        "",
        "```sql",
        "SELECT T.NOMETAB    AS TABELA,",
        "       T.DESCRTAB   AS DESCRICAO_TABELA,",
        "       T.TIPONUMERACAO AS TIPO_NUMERACAO,",
        "       C.ORDEM      AS ORDEM_CAMPO,",
        "       C.NOMECAMPO  AS CAMPO,",
        "       C.DESCRCAMPO AS DESCRICAO_CAMPO,",
        "       C.TIPCAMPO   AS TIPO_CAMPO,",
        "       C.TAMANHO    AS TAMANHO,",
        "       C.CALCULADO  AS CALCULADO,",
        "       C.ADICIONAL  AS ADICIONAL,",
        "       CASE WHEN C.ADICIONAL = 'S'",
        "              OR C.NOMECAMPO LIKE 'AD\\_%' ESCAPE '\\'",
        "              OR T.NOMETAB  LIKE 'AD\\_%' ESCAPE '\\'",
        "            THEN 'S' ELSE 'N' END AS CUSTOMIZADO",
        "  FROM TDDTAB T",
        "  JOIN TDDCAM C ON C.NOMETAB = T.NOMETAB",
        " ORDER BY T.NOMETAB, C.ORDEM, C.NOMECAMPO;",
        "```",
        "",
        "As colunas de `TDDTAB`/`TDDCAM` estão verificadas em instalação sobre Oracle 19c",
        "(ver `stacks-java-sankhya-dicionario.md`). A regra de `CUSTOMIZADO` acima é a",
        "convenção do padrão, não um campo do dicionário — confira se ela corresponde ao",
        "critério usado na sua exportação.",
        "",
    ]
    (destino / f"{PREFIXO}-README.md").write_text("\n".join(linhas), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", type=Path, default=CSV_PADRAO)
    args = ap.parse_args()

    linhas = ler(args.csv)
    classificacao, marcadores, faltando = carregar_prefixos(
        [l["TABELA"] for l in linhas]
    )
    marcados = 0

    def e_publico(linha: dict) -> bool:
        nonlocal marcados
        if linha["CUSTOMIZADO"] == "S":
            return False
        nome = f"{linha['TABELA']} {linha['CAMPO']}".upper()
        if any(m in nome for m in marcadores):
            marcados += 1
            return False
        # Prefixo não classificado fica privado: errar para o lado de não publicar.
        return classificacao.get(prefixo_de(linha["TABELA"]), "privado") == "publico"

    produto, custom = [], []
    for linha in linhas:
        (produto if e_publico(linha) else custom).append(linha)

    tabelas = agrupar(produto)
    arquivos = fatiar(tabelas)
    limpar(OUT_WEB)
    for nome, blocos in arquivos.items():
        conteudo = f"# {nome[:-3]}\n\n{CABECALHO}\n" + "\n".join(blocos)
        (OUT_WEB / nome).write_text(conteudo, encoding="utf-8")
    escrever_indice(OUT_WEB, arquivos, tabelas)

    OUT_LOCAL.mkdir(parents=True, exist_ok=True)
    alvo_local = OUT_LOCAL / f"{PREFIXO}-instalacao.md"
    if custom:
        tabelas_custom = agrupar(custom)
        conteudo = (
            f"# {PREFIXO}-instalacao\n\n{CABECALHO_LOCAL}\n"
            + "\n".join(render(n, t) for n, t in tabelas_custom.items())
        )
        alvo_local.write_text(conteudo, encoding="utf-8")
    elif alvo_local.exists():
        alvo_local.unlink()

    total_web = sum(
        (OUT_WEB / n).stat().st_size for n in list(arquivos) + [f"{PREFIXO}-README.md"]
    )
    print(f"dist/web/dicionario/: {len(arquivos) + 1} arquivos, "
          f"{len(tabelas)} tabelas, {len(produto)} campos, {total_web / 1024:.0f} KB")
    if custom:
        print(f"dist/local/{alvo_local.name}: {len(agrupar(custom))} tabelas, "
              f"{len(custom)} campos da instalação — NÃO versionar")
    if marcados:
        print(f"{marcados} campos retidos por marcador de organização "
              f"({', '.join(sorted(marcadores))})")
    elif not marcadores:
        print(
            "AVISO: nenhum `marcador` declarado. Se a sua instalação usa a sigla da\n"
            "       empresa em nome de campo ou tabela (TGFCAB.SIGLACODEMPAUT,\n"
            "       TGFCAB_SIGLA), esses campos estão indo para a saída publicável.\n"
            f"       Declare a sigla em {ARQ_PREFIXOS}.",
            file=sys.stderr,
        )
    if faltando:
        print(
            f"AVISO: {len(faltando)} prefixos sem classificação, tratados como "
            f"privados: {', '.join(faltando)}\n"
            f"       Classifique-os em {ARQ_PREFIXOS}.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
