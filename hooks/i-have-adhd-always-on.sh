#!/usr/bin/env sh
# SessionStart hook de Claude Code: inyecta las reglas de i-have-adhd en cada sesión.
# Adaptado de https://github.com/ayghri/i-have-adhd (MIT), sin el archivo flag de opt-in:
# install.sh lo registra por defecto. Nunca bloquea el inicio: cualquier fallo sale con 0.

skill_path="$(dirname -- "$0")/../skills/i-have-adhd/SKILL.md"
[ -f "$skill_path" ] || exit 0

# Quita el frontmatter YAML inicial (--- ... ---).
body=$(awk 'NR == 1 && /^---[[:space:]]*$/ { fm = 1; next }
  fm && /^---[[:space:]]*$/ { fm = 0; next }
  !fm' "$skill_path") || exit 0

printf 'ADHD MODE ACTIVE (always-on). The ruleset below applies to every response. "stop adhd mode" turns it off for this session.\n\n%s\n' "$body"
