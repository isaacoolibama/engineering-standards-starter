#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

required=(
  "README.md"
  "AGENTS.md"
  "CLAUDE.md"
  "references/sources.yml"
  "stacks/java-sankhya/README.md"
)

for file in "${required[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "MISSING: $file" >&2
    exit 1
  fi
done

if grep -RniE --exclude='validate.sh' --exclude-dir='.git' 'JSF Florestal|JSF Empreendimentos' .; then
  echo "ERROR: organization-specific reference found" >&2
  exit 1
fi

python -c "from pathlib import Path; t=Path('references/sources.yml').read_text(encoding='utf-8'); assert 'sources:' in t and 'sankhya:' in t and 'security:' in t; print('sources.yml: structural check OK')"

# Links: internos sempre; externos so quando LINK_CHECK=1 (evita depender de rede no uso local).
if [[ "${LINK_CHECK:-0}" == "1" ]]; then
  "$ROOT/scripts/check-links.sh"
else
  "$ROOT/scripts/check-links.sh" --offline
fi

echo "Engineering Standards validation: OK"
