#!/usr/bin/env bash
# Gera tudo que vai para um Project do Claude ou do ChatGPT e diz o que subir.
#
# Um comando só, porque a montagem do pacote web tem três etapas que precisam
# acontecer juntas: os documentos do padrão, o dicionário da instalação e a
# validação que impede publicar customização por engano.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

CSV="${1:-sankhya-dicionario-instalacao.csv}"

echo "== 1/3  Documentos do padrão =="
python3 scripts/build-web.py

echo
echo "== 2/3  Dicionário Sankhya =="
if [[ -f "$CSV" ]]; then
  python3 scripts/build-dicionario.py --csv "$CSV"
else
  echo "  $CSV não encontrado — pulando."
  echo "  Para gerar: exporte o dicionário do banco com a query de"
  echo "  stacks/java-sankhya/dicionario.md e salve como CSV nesse caminho."
fi

echo
echo "== 3/3  Validação =="
scripts/validate.sh | tail -1

cat <<'FIM'

────────────────────────────────────────────────────────────────────
O QUE SUBIR NO PROJECT (Claude: Project knowledge / ChatGPT: Arquivos)

  1. dist/web/bundles/nucleo.md      regras que valem em qualquer stack
  2. dist/web/bundles/sankhya.md     padrão Sankhya, Java, PL/SQL e SQL
  3. dist/web/dicionario/*.md        tabelas e campos do produto

  Suba também backend.md, frontend.md ou linguagens.md se a equipe
  trabalhar nessas stacks.

O QUE COLAR EM INSTRUÇÕES

  Claude   -> adapters/claude-project-instructions.md
  ChatGPT  -> adapters/chatgpt-project-instructions.md
  (cole a partir da linha após o separador ---, não o cabeçalho)

O DICIONÁRIO DA INSTALAÇÃO

  dist/local/sankhya-dicionario-instalacao.md
    Campos AD_, campos com a sigla da empresa e tabelas próprias.
    SUBA no Project da equipe — é o que permite ao assistente
    confirmar as suas customizações.
    NÃO versione, NÃO publique fora da empresa: esses campos não
    existem em outra instalação e expõem o esquema interno.

  O CSV bruto fica só na sua máquina.
────────────────────────────────────────────────────────────────────
FIM
