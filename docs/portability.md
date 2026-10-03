# Portabilidad

## Contrato común

Cada skill se distribuye como una carpeta con `SKILL.md`, frontmatter `name` y `description`, y sus recursos relativos. Es el formato [Agent Skills](https://agentskills.io/specification). El contenido portable no depende de una marca de modelo ni de nombres de herramientas de un runtime.

`agents/openai.yaml` es un complemento opcional de Codex. Las instrucciones necesarias para ejecutar una skill viven en `SKILL.md`, de modo que otro agente pueda ignorar ese YAML. Tampoco usamos interpolación de comandos o variables exclusivas de Claude en el núcleo de las tres skills principales.

Portabilidad del formato no garantiza idéntico comportamiento ni descubrimiento automático. Un agente necesita poder leer archivos y, para trabajar sobre repositorios, inspeccionar Git. La publicación requiere además una integración con el proveedor de PRs.

## Usar desde cualquier agente

La entrada explícita evita ambigüedad sobre qué versión estás probando:

```text
Lee skills/code-review/SKILL.md de este checkout y úsala para revisar
el repositorio <ruta>, comparando <base> con <head>.
```

Para editar la skill en Conductor:

```text
Edita skills/code-review/SKILL.md de este workspace para mejorar <criterio>.
Lee AGENTS.md. Compara el comportamiento anterior y propuesto sobre <caso>.
```

## Descubrimiento por herramienta

| Herramienta | Instalación | Invocación |
| --- | --- | --- |
| Codex | `~/.agents/skills/<nombre>` para uso personal; `.agents/skills/<nombre>` dentro de un proyecto | `$code-review` o ruta explícita |
| Claude Code | `~/.claude/skills/<nombre>` para uso personal; `.claude/skills/<nombre>` dentro de un proyecto | `/code-review` o ruta explícita |
| Otro agente | Su directorio compatible con Agent Skills, o adjuntar `SKILL.md` y sus referencias | Según su mecanismo; la ruta explícita sirve si puede leer archivos |

Fuentes: [Codex](https://learn.chatgpt.com/es-419/docs/build-skills), [Claude Code](https://code.claude.com/docs/en/skills). Rutas verificadas el 2026-09-14.

### Instalación

Corre `./install.sh` desde el checkout principal (`~/conductor/repos/agents` en esta máquina). Es idempotente: repítelo al agregar o quitar una skill, o si mueves el repo. Se niega a correr desde un worktree de Conductor, porque los enlaces quedarían apuntando a una copia temporal.

| Qué | Claude Code | Codex |
| --- | --- | --- |
| Skills | Un symlink por skill en `~/.claude/skills/<nombre>`; Claude Code no busca en subcarpetas | `~/.agents/skills` enlaza a `skills/` |
| `i-have-adhd` siempre activo | Hook `SessionStart` en `~/.claude/settings.json` que ejecuta `hooks/i-have-adhd-always-on.sh` | Bloque entre marcadores `i-have-adhd` en `~/.codex/AGENTS.md` |
| RTK | `brew install rtk` si falta; `rtk init -g --auto-patch` agrega su hook `PreToolUse` | `rtk init -g --codex --auto-patch` |

`--no-adhd-always-on` retira el hook y el bloque de Codex; la skill sigue disponible con `/i-have-adhd`. En una sesión, "stop adhd mode" lo apaga. `--skip-rtk` omite RTK. El script no toca carpetas reales con el mismo nombre que una skill; avisa y las omite.

Incorporar un cambio a `main` en el checkout principal actualiza ambas instalaciones, porque leen el repo mediante enlaces. La `code-review` personal reemplaza el comando integrado `/code-review` de Claude Code; el alias `/review` sigue ejecutando el integrado.

En Conductor, el directorio de trabajo es otra copia de Git. Invoca la ruta de ese workspace para probar un draft: una skill descubierta globalmente puede seguir leyendo la versión del checkout principal.

## Skills importadas

Las skills fuera del grupo principal siguen como importadas, sin promesa de portabilidad auditada. Algunas nombran herramientas de Claude, exigen subagentes o dependen del setup de Matt Pocock. Migra una cuando la vayas a usar: conserva el comportamiento útil, elimina dependencias implícitas y prueba la nueva versión.

`.skill-lock.json` registra instalaciones de terceros, no es un manifiesto de esta colección personal. Sus hashes reflejan el contenido importado, no las modificaciones propias. Evita actualizar automáticamente `code-review` desde su origen: ahora es una variante local.
