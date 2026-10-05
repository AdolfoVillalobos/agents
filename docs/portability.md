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

Corre `make install` (o `./install.sh`) desde el checkout principal; localízalo con `git worktree list`. El instalador se niega a correr desde un worktree temporal. En esta máquina el checkout principal sigue en `~/.agents`.

Se comparte la carpeta completa:

```text
~/.claude/skills -> ~/.agents/skills -> <checkout principal>/skills
```

Cuando el checkout principal es `~/.agents`, su carpeta `skills` ya es el destino real: se conserva y solo Claude necesita el enlace. Las skills nuevas quedan disponibles en ambas rutas sin reinstalar ni crear enlaces individuales. También se conservan archivos sin seguimiento, como `skills/synced/`.

El instalador acepta una carpeta real o un enlace que ya resuelva a esta colección. Si encuentra otra colección o un enlace roto, se detiene antes de modificar la configuración: primero hay que integrar esas skills. No elimina carpetas ni sustituye silenciosamente sus destinos. En esta máquina, `plan-project` y `review-pr` siguen conservadas en la carpeta antigua de `claude-config`; no se incorporan automáticamente a la colección compartida.

| Qué | Claude Code | Codex |
| --- | --- | --- |
| Skills | Un enlace de carpeta a `~/.agents/skills` | Carpeta real del checkout o un enlace a `skills/` |
| `i-have-adhd` siempre activo | Un hook `SessionStart` que lee `hooks/i-have-adhd-always-on.sh` | Bloque entre marcadores en `~/.codex/AGENTS.md` |
| RTK | `brew install rtk` si falta; `rtk init -g --auto-patch` | `rtk init -g --codex` |

Antes de actualizar configuración, guarda una copia en `~/.agents/backups/install-…`. Los respaldos y `skills/synced/` están excluidos de Git. Conserva los demás ajustes y hooks, incluidos los de RTK. Retira invocaciones simples de `i-have-adhd-always-on.sh` y `adhd-ruleset-reminder.sh`, directamente o mediante `sh`/`bash`, con rutas sin comillas o entre comillas simples o dobles. Si un hook combina ADHD con otros comandos, redirecciones o una sintaxis no reconocida, se detiene sin modificar la configuración: hay que separar la invocación ADHD en su propio hook. También rechaza JSON inválido o un bloque de Codex incompleto antes de escribir cambios.

`make adhd-on-demand` retira los hooks ADHD conocidos y el bloque de Codex; la skill sigue disponible bajo demanda. En una sesión, «stop adhd mode» lo apaga. `make install-no-rtk` omite la instalación y configuración de RTK. Los cambios de contenido en `i-have-adhd` requieren repetir el instalador para refrescar el bloque copiado de Codex.

`make test-install` prueba el script en repositorios y configuraciones temporales. Para esa prueba, `AGENT_INSTALL_ROOT` redirige las tres carpetas de configuración y exige `--skip-rtk`, porque RTK gestiona sus propias rutas globales. Acepta rutas absolutas o relativas al directorio desde el que se ejecuta; los enlaces siempre usan destinos absolutos. No cambia `HOME` ni usa tus configuraciones reales. La suite verifica enlaces, preservación de skills y configuración, migración de hooks con comillas, rechazo de comandos compuestos sin cambios parciales, reinstalación y errores de entrada; no ejecuta los modelos ni instala RTK.

Incorporar cambios al checkout principal actualiza los archivos que leen ambos agentes. Abre una sesión nueva para comprobar su descubrimiento; una sesión existente puede conservar instrucciones previas.

### Review en GitHub

El workflow de review utiliza `skills/code-review/SKILL.md` de la revisión base del PR, con pasadas secuenciales y comentarios en español. Las modificaciones de esa skill dentro del PR son contenido a revisar; el workflow no las usa como sus propias instrucciones. Conservamos también el workflow que responde a menciones `@claude`.

En Conductor, el directorio de trabajo es otra copia de Git. Invoca la ruta de ese workspace para probar un draft: una skill descubierta globalmente puede seguir leyendo la versión del checkout principal.

## Skills importadas

Las skills fuera del grupo principal siguen como importadas, sin promesa de portabilidad auditada. Algunas nombran herramientas de Claude, exigen subagentes o dependen del setup de Matt Pocock. Migra una cuando la vayas a usar: conserva el comportamiento útil, elimina dependencias implícitas y prueba la nueva versión.

`.skill-lock.json` registra instalaciones de terceros, no es un manifiesto de esta colección personal. Sus hashes reflejan el contenido importado, no las modificaciones propias. Evita actualizar automáticamente `code-review` desde su origen: ahora es una variante local.
