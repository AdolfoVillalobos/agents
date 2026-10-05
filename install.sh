#!/usr/bin/env bash
# Instala esta colección para Claude Code y Codex. Es idempotente: vuelve a correrlo
# después de agregar o quitar skills, o si mueves el checkout.
#
#   ./install.sh                     skills + i-have-adhd siempre activo + RTK
#   ./install.sh --no-adhd-always-on deja i-have-adhd solo bajo demanda (/i-have-adhd)
#   ./install.sh --skip-rtk          no instala ni configura RTK
set -euo pipefail

adhd_always_on=1
rtk=1
for arg in "$@"; do
  case "$arg" in
    --no-adhd-always-on) adhd_always_on=0 ;;
    --skip-rtk) rtk=0 ;;
    *) echo "Opción desconocida: $arg" >&2; exit 2 ;;
  esac
done

REPO=$(cd "$(dirname "$0")" && pwd -P)
CLAUDE_DIR=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
CODEX_DIR=${CODEX_HOME:-$HOME/.codex}

# Un worktree de Conductor desaparece al archivarlo; los enlaces deben apuntar al checkout principal.
if [ "$(git -C "$REPO" rev-parse --path-format=absolute --git-dir)" != "$(git -C "$REPO" rev-parse --path-format=absolute --git-common-dir)" ]; then
  main=$(git -C "$REPO" worktree list --porcelain | sed -n '1s/^worktree //p')
  echo "Esto es un worktree temporal. Incorpora el cambio a main y corre $main/install.sh" >&2
  exit 1
fi

command -v jq >/dev/null || { echo "Falta jq (brew install jq)." >&2; exit 1; }

# 1. Skills: Claude Code solo descubre ~/.claude/skills/<nombre>, así que se enlaza cada una.
mkdir -p "$CLAUDE_DIR/skills"
for dir in "$REPO"/skills/*/; do
  name=$(basename "$dir")
  link="$CLAUDE_DIR/skills/$name"
  if [ -e "$link" ] && [ ! -L "$link" ]; then
    echo "Omitida $name: $link existe y no es un enlace." >&2
    continue
  fi
  ln -sfn "${dir%/}" "$link"
done
# Enlaces a skills que ya no existen en el repo.
for link in "$CLAUDE_DIR"/skills/*; do
  if [ -L "$link" ] && [ ! -e "$link" ] && [[ "$(readlink "$link")" == "$REPO/skills/"* ]]; then
    rm "$link"
  fi
done

mkdir -p "$HOME/.agents"
if [ -e "$HOME/.agents/skills" ] && [ ! -L "$HOME/.agents/skills" ]; then
  echo "Omitido Codex: ~/.agents/skills existe y no es un enlace." >&2
else
  ln -sfn "$REPO/skills" "$HOME/.agents/skills"
fi
echo "Skills enlazadas: $(ls -d "$REPO"/skills/*/ | wc -l | tr -d ' ')"

# 2. i-have-adhd siempre activo.
# Claude Code: hook SessionStart que inyecta SKILL.md. Reemplaza registros previos de este hook.
settings="$CLAUDE_DIR/settings.json"
[ -f "$settings" ] || echo '{}' >"$settings"
hook_cmd="sh \"$REPO/hooks/i-have-adhd-always-on.sh\""
tmp=$(mktemp)
jq --arg cmd "$hook_cmd" --argjson on "$adhd_always_on" '
  .hooks.SessionStart = (
    [ .hooks.SessionStart[]?
      | .hooks |= map(select(.command | test("i-have-adhd-always-on\\.sh") | not))
      | select(.hooks | length > 0) ]
    + if $on == 1 then
        [{matcher: "startup|resume|clear|compact",
          hooks: [{type: "command", command: $cmd, timeout: 30}]}]
      else [] end)
  | if .hooks.SessionStart == [] then del(.hooks.SessionStart) else . end
  | if .hooks == {} then del(.hooks) else . end' "$settings" >"$tmp"
mv "$tmp" "$settings"

# Codex: no tiene un hook equivalente, así que el texto va en ~/.codex/AGENTS.md entre marcadores.
agents_md="$CODEX_DIR/AGENTS.md"
mkdir -p "$CODEX_DIR"
touch "$agents_md"
tmp=$(mktemp)
awk '/^<!-- i-have-adhd:start -->$/ { skip = 1 } !skip { print } /^<!-- i-have-adhd:end -->$/ { skip = 0 }' "$agents_md" >"$tmp"
if [ "$adhd_always_on" = 1 ]; then
  {
    echo '<!-- i-have-adhd:start -->'
    sh "$REPO/hooks/i-have-adhd-always-on.sh"
    echo '<!-- i-have-adhd:end -->'
  } >>"$tmp"
  echo "i-have-adhd: siempre activo en Claude Code y Codex"
else
  echo "i-have-adhd: bajo demanda (/i-have-adhd o \$i-have-adhd)"
fi
mv "$tmp" "$agents_md"

# 3. RTK (Rust Token Killer): binario + hooks PreToolUse propios de RTK.
if [ "$rtk" = 1 ]; then
  if ! rtk gain >/dev/null 2>&1; then
    if command -v rtk >/dev/null; then
      echo "El rtk instalado no es Rust Token Killer (falta 'rtk gain'). Desinstálalo y vuelve a correr." >&2
      exit 1
    fi
    command -v brew >/dev/null || { echo "Instala RTK: https://github.com/rtk-ai/rtk#installation" >&2; exit 1; }
    brew install rtk
  fi
  rtk init -g --auto-patch
  rtk init -g --codex  # rtk no acepta --auto-patch con --codex
fi

echo "Listo. Reinicia Claude Code y Codex para cargar los cambios."
