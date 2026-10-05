#!/usr/bin/env bash
# Instala la colección compartida, ADHD siempre activo y RTK.
# AGENT_INSTALL_ROOT permite probar en una raíz aislada; requiere --skip-rtk.
set -euo pipefail
umask 077

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
if [ -n "${AGENT_INSTALL_ROOT:-}" ]; then
  [ "$rtk" = 0 ] || { echo "AGENT_INSTALL_ROOT requiere --skip-rtk: RTK configura rutas globales." >&2; exit 2; }
  install_root="$AGENT_INSTALL_ROOT"
  case "$install_root" in
    /*) ;;
    *) install_root="$(pwd -P)/$install_root" ;;
  esac
  CLAUDE_DIR="$install_root/.claude"
  CODEX_DIR="$install_root/.codex"
  AGENTS_DIR="$install_root/.agents"
else
  CLAUDE_DIR=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
  CODEX_DIR=${CODEX_HOME:-$HOME/.codex}
  AGENTS_DIR="$HOME/.agents"
fi

# Los enlaces deben sobrevivir al archivado de un worktree.
if [ "$(git -C "$REPO" rev-parse --path-format=absolute --git-dir)" != "$(git -C "$REPO" rev-parse --path-format=absolute --git-common-dir)" ]; then
  main=$(git -C "$REPO" worktree list --porcelain | sed -n '1s/^worktree //p')
  echo "Esto es un worktree temporal. Incorpora el cambio al checkout principal y corre $main/install.sh" >&2
  exit 1
fi
command -v jq >/dev/null || { echo "Falta jq (brew install jq)." >&2; exit 1; }

# Acepta la carpeta real del repo o enlaces que ya resuelven a ella. Nunca oculta
# una colección distinta, incluidas skills sincronizadas o sin seguimiento en Git.
check_skill_path() {
  local path=$1
  if [ -e "$path" ] || [ -L "$path" ]; then
    if ! [ "$path" -ef "$REPO/skills" ]; then
      echo "Conservado $path: contiene o apunta a otra colección. Integra sus skills antes de cambiar el enlace." >&2
      return 1
    fi
  fi
}
check_skill_path "$AGENTS_DIR/skills"
check_skill_path "$CLAUDE_DIR/skills"

settings="$CLAUDE_DIR/settings.json"
agents_md="$CODEX_DIR/AGENTS.md"
settings_tmp=$(mktemp)
agents_tmp=$(mktemp)
trap 'rm -f "$settings_tmp" "$agents_tmp"' EXIT
hook_cmd="sh \"$REPO/hooks/i-have-adhd-always-on.sh\""

# Migra invocaciones simples, sin interpretar ni ejecutar el comando guardado.
# Ante referencias ambiguas, falla antes de escribir en lugar de borrar otros comandos.
jq_filter='
  def managed_adhd:
    (.command? // "") as $command
    | "(?:i-have-adhd-always-on|adhd-ruleset-reminder)[.]sh" as $script
    | ("(?:[^\\s\u0027\"\\\\$`;&|<>()*?\\[\\]{}#]+/)?" + $script) as $bare
    | ("\u0027(?:[^\u0027\\r\\n]*/)?" + $script + "\u0027") as $single
    | ("\"(?:[^\"\\\\$`\\r\\n]*/)?" + $script + "\"") as $double
    | ("\\A\\s*(?:(?:/bin/|/usr/bin/)?(?:sh|bash)\\s+)?(?:" +
      $bare + "|" + $single + "|" + $double + ")\\s*\\z") as $simple
    | if ($command | test($script) | not) then false
      elif ($command | test($simple)) then true
      else error("Hook ADHD compuesto o no reconocido: separa su invocación en un hook propio antes de instalar; no se modificó la configuración.")
      end;
  .hooks = ((.hooks // {}) | with_entries(
    .value |= map(.hooks |= map(select(managed_adhd | not)) | select(.hooks | length > 0))
    | select(.value | length > 0)))
  | if $on == 1 then
      .hooks.SessionStart = ((.hooks.SessionStart // []) +
        [{matcher: "startup|resume|clear|compact",
          hooks: [{type: "command", command: $cmd, timeout: 30}]}])
    else . end
  | if .hooks == {} then del(.hooks) else . end'
if [ -f "$settings" ]; then
  jq --arg cmd "$hook_cmd" --argjson on "$adhd_always_on" "$jq_filter" "$settings" >"$settings_tmp"
else
  printf '{}\n' | jq --arg cmd "$hook_cmd" --argjson on "$adhd_always_on" "$jq_filter" >"$settings_tmp"
fi

# Rechaza un bloque incompleto antes de modificar configuración alguna.
if [ -f "$agents_md" ]; then
  awk '
    /^<!-- i-have-adhd:start -->$/ { if (skip) exit 1; skip = 1; next }
    /^<!-- i-have-adhd:end -->$/ { if (!skip) exit 1; skip = 0; next }
    !skip { print }
    END { if (skip) exit 1 }
  ' "$agents_md" >"$agents_tmp" || { echo "Bloque ADHD incompleto en $agents_md; no se modificó." >&2; exit 1; }
fi
if [ "$adhd_always_on" = 1 ]; then
  {
    echo '<!-- i-have-adhd:start -->'
    sh "$REPO/hooks/i-have-adhd-always-on.sh"
    echo '<!-- i-have-adhd:end -->'
  } >>"$agents_tmp"
fi

# Respalda los archivos que este instalador o RTK pueden actualizar.
mkdir -p "$AGENTS_DIR/backups"
backup=$(mktemp -d "$AGENTS_DIR/backups/install-$(date +%Y%m%d-%H%M%S)-XXXXXX")
mkdir -p "$backup/claude" "$backup/codex"
for file in settings.json CLAUDE.md; do
  [ ! -f "$CLAUDE_DIR/$file" ] || cp -p "$CLAUDE_DIR/$file" "$backup/claude/$file"
done
for file in AGENTS.md hooks.json config.toml; do
  [ ! -f "$CODEX_DIR/$file" ] || cp -p "$CODEX_DIR/$file" "$backup/codex/$file"
done

mkdir -p "$CLAUDE_DIR" "$CODEX_DIR" "$AGENTS_DIR"
# Un único enlace de carpeta por consumidor; la carpeta real del repo se conserva.
if [ ! -e "$AGENTS_DIR/skills" ]; then
  ln -s "$REPO/skills" "$AGENTS_DIR/skills"
fi
if [ ! -e "$CLAUDE_DIR/skills" ]; then
  ln -s "$AGENTS_DIR/skills" "$CLAUDE_DIR/skills"
fi
# Escribe a través de enlaces de configuración existentes sin reemplazarlos.
cat "$settings_tmp" >"$settings"
cat "$agents_tmp" >"$agents_md"
echo "Skills compartidas. Respaldo: $backup"
if [ "$adhd_always_on" = 1 ]; then
  echo "i-have-adhd: siempre activo, sin duplicar hooks conocidos"
else
  echo "i-have-adhd: bajo demanda"
fi

if [ "$rtk" = 1 ]; then
  if ! rtk gain >/dev/null 2>&1; then
    if command -v rtk >/dev/null; then
      echo "El rtk instalado no es Rust Token Killer (falta 'rtk gain')." >&2
      exit 1
    fi
    command -v brew >/dev/null || { echo "Instala RTK: https://github.com/rtk-ai/rtk#installation" >&2; exit 1; }
    brew install rtk
  fi
  rtk init -g --auto-patch
  rtk init -g --codex
fi

echo "Listo. Abre una sesión nueva de Claude Code o Codex para cargar los cambios."
