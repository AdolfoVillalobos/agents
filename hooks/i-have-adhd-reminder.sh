#!/usr/bin/env sh
# UserPromptSubmit: refresca solo el recordatorio, sin reactivar un modo apagado.
skill_path="$(dirname -- "$0")/../modules/personal/skills/i-have-adhd/SKILL.md"
[ -f "$skill_path" ] || exit 0

awk '
  /^## Turn reminder$/ { show = 1; next }
  show && /^## / { exit }
  show { print }
' "$skill_path"
