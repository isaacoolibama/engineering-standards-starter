#!/usr/bin/env bash
# Valida referências internas (arquivos) e links externos (HTTP) do repositório.
# Uso: scripts/check-links.sh [--offline]
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PY="$(command -v python3 || command -v python)"
if [[ -z "$PY" ]]; then echo "python3 nao encontrado" >&2; exit 2; fi

fail=0

echo "== Referencias internas =="
"$PY" - <<'PYEOF' || fail=1
import os, re, sys
root = os.getcwd()
pat = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
broken = []
for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in ('.git', 'node_modules')]
    for fn in filenames:
        if not fn.endswith('.md'):
            continue
        path = os.path.join(dirpath, fn)
        rel = os.path.relpath(path, root)
        with open(path, encoding='utf-8') as fh:
            for lineno, line in enumerate(fh, 1):
                for target in pat.findall(line):
                    if re.match(r'^(https?:|mailto:|#)', target):
                        continue
                    clean = target.split('#')[0].strip()
                    if not clean:
                        continue
                    resolved = os.path.normpath(os.path.join(dirpath, clean))
                    if not os.path.exists(resolved):
                        broken.append(f"  QUEBRADO: {rel}:{lineno} -> {target}")
print("\n".join(broken) if broken else "  ok")
sys.exit(1 if broken else 0)
PYEOF

if [[ "${1:-}" == "--offline" ]]; then
  echo "== Links externos: pulado (--offline) =="
  exit $fail
fi

echo "== Links externos =="
urls="$(grep -rhoE 'https?://[^ )<>"]+' --include='*.md' --include='*.yml' . \
        | sed -E 's/[.,;:]+$//' | sort -u)"
total=$(grep -c . <<< "$urls")
i=0
while IFS= read -r url; do
  [[ -z "$url" ]] && continue
  i=$((i+1))
  code=$(curl -sS -o /dev/null -w '%{http_code}' -L --max-time 25 \
         -A 'Mozilla/5.0 (compatible; standards-link-check)' "$url" 2>/dev/null)
  case "$code" in
    2*|3*)       printf '  [%2d/%2d] %s  %s\n' "$i" "$total" "$code" "$url" ;;
    403|405|429) printf '  [%2d/%2d] %s  %s  (bloqueio de bot, provavel OK)\n' "$i" "$total" "$code" "$url" ;;
    *)           printf '  [%2d/%2d] %s  %s  <== FALHOU\n' "$i" "$total" "${code:-000}" "$url"; fail=1 ;;
  esac
done <<< "$urls"
exit $fail
