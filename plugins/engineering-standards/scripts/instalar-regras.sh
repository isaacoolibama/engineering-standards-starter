#!/usr/bin/env bash
# Instala as regras path-scoped em ~/.claude/rules/engineering-standards.
# Funciona tanto a partir do plugin instalado quanto do repositório clonado.
set -euo pipefail

ORIGEM="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}/rules"

if [[ ! -d "$ORIGEM" ]]; then
  echo "ERRO: diretório de regras não encontrado em $ORIGEM" >&2
  exit 1
fi

DESTINO="$HOME/.claude/rules/engineering-standards"
mkdir -p "$HOME/.claude/rules"
rm -rf "$DESTINO"
cp -r "$ORIGEM" "$DESTINO"

n=$(find "$DESTINO" -name '*.md' | wc -l)
echo "$n regras instaladas em $DESTINO"
find "$DESTINO" -name '*.md' -printf '  %f\n' | sort
echo
echo "Abra uma sessão nova e rode /context para confirmar."
echo "Regras com paths: só aparecem depois de abrir um arquivo do tipo correspondente."
