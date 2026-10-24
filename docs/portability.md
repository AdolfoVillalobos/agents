# Portabilidad

## Contrato común

Cada skill se distribuye como una carpeta con `SKILL.md`, frontmatter `name` y `description`, y sus recursos relativos. Es el formato [Agent Skills](https://agentskills.io/specification). El contenido portable no depende de una marca de modelo ni de nombres de herramientas de un runtime.

`agents/openai.yaml` es un complemento opcional de Codex. Las instrucciones necesarias para ejecutar una skill viven en `SKILL.md`, de modo que otro agente pueda ignorar ese YAML. Tampoco usamos interpolación de comandos o variables exclusivas de Claude en el núcleo de las tres skills principales.

Portabilidad del formato no garantiza idéntico comportamiento ni descubrimiento automático. Un agente necesita poder leer archivos y, para trabajar sobre repositorios, inspeccionar Git. La publicación requiere además una integración con el proveedor de PRs.

Las skills `review-design`, `review-qa`, `review-readiness` y `review-comments` se distribuyen con esta colección. Las tres primeras comparten recursos en `skills/code-review/references/` mediante rutas relativas. `review-readiness` también consulta `skills/create-pr/SKILL.md` cuando redacta una descripción. `review-comments` consulta ese mismo protocolo y, si todavía no hay hallazgos, la skill del pase que corresponda. También trae `references/github-posting.md`, que se lee solo al publicar en GitHub. Para trasladarlas, conserva esas carpetas hermanas. Copiar solo `review-comments` deja el protocolo sin resolver. No requieren adaptadores ni subagentes. Esto describe su estructura, no una validación de comportamiento en Claude o Codex.

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
| `i-have-adhd` siempre activo | `SessionStart` carga las reglas; `UserPromptSubmit` refresca un recordatorio breve | Bloque entre marcadores en `~/.codex/AGENTS.md` |
| RTK | `brew install rtk` si falta; `rtk init -g --auto-patch` | `rtk init -g --codex` |

Antes de actualizar configuración, guarda una copia en `~/.agents/backups/install-…`. Los respaldos y `skills/synced/` están excluidos de Git. Conserva los demás ajustes y hooks, incluidos los de RTK. Retira invocaciones simples de `i-have-adhd-always-on.sh` y `adhd-ruleset-reminder.sh`, directamente o mediante `sh`/`bash`, con rutas sin comillas o entre comillas simples o dobles. Si un hook combina ADHD con otros comandos, redirecciones o una sintaxis no reconocida, se detiene sin modificar la configuración: hay que separar la invocación ADHD en su propio hook. También rechaza JSON inválido o un bloque de Codex incompleto antes de escribir cambios.

`make adhd-on-demand` retira los hooks ADHD conocidos y el bloque de Codex; la skill sigue disponible bajo demanda. En una sesión, «stop adhd mode» lo apaga. `make install-no-rtk` omite la instalación y configuración de RTK. Los cambios de contenido en `i-have-adhd` requieren repetir el instalador para refrescar el bloque copiado de Codex.

El recordatorio de Claude se extrae de `Turn reminder` en `skills/i-have-adhd/SKILL.md` en cada mensaje. Refuerza el alcance de la pregunta actual sin repetir las reglas completas ni reactivar el modo después de «stop adhd mode». Que un hook entregue las instrucciones demuestra su carga, no garantiza que el modelo las siga: revisa también la respuesta. Los [casos de evaluación](../skills/i-have-adhd/evaluacion.md) separan ambas comprobaciones.

Si el plugin anterior de ADHD tiene la bandera `~/.claude/.i-have-adhd-always`, el instalador la mueve al respaldo después de escribir la configuración. El plugin se conserva; su inyección automática queda desactivada para que esta colección controle ADHD sin duplicarlo, también al elegir el modo bajo demanda.

`make test-install` prueba el script en repositorios y configuraciones temporales. Para esa prueba, `AGENT_INSTALL_ROOT` redirige las tres carpetas de configuración y exige `--skip-rtk`, porque RTK gestiona sus propias rutas globales. Acepta rutas absolutas o relativas al directorio desde el que se ejecuta; los enlaces siempre usan destinos absolutos. No cambia `HOME` ni usa tus configuraciones reales. La suite verifica enlaces, preservación de skills y configuración, migración de hooks con comillas, rechazo de comandos compuestos sin cambios parciales, reinstalación y errores de entrada; no ejecuta los modelos ni instala RTK.

Incorporar cambios al checkout principal actualiza los archivos que leen ambos agentes. Abre una sesión nueva para comprobar su descubrimiento; una sesión existente puede conservar instrucciones previas.

### Review en GitHub

El workflow de review corre Codex con `openai/codex-action` y el perfil `:read-only`. Copia `skills/code-review/SKILL.md` de la revisión base del PR, hace las pasadas en secuencia y publica la revisión en español. Las modificaciones de esa skill dentro del PR son contenido a revisar; el workflow no las usa como sus propias instrucciones. Codex no comenta ni escribe en el repositorio: un job posterior publica la revisión completa como un solo comentario. Hace falta el secreto `OPENAI_API_KEY`. Conservamos también el workflow que responde a menciones `@claude`.

En Conductor, el directorio de trabajo es otra copia de Git. Invoca la ruta de ese workspace para probar un draft: una skill descubierta globalmente puede seguir leyendo la versión del checkout principal.

## Skills importadas

La colección de [Addy Osmani](addyosmani-agent-skills.md) conserva la estructura original: `skills/<nombre>/` y siete documentos compartidos en `references/`, en la raíz del repo. Las rutas `../../references/…` de cada skill se resuelven contra esa estructura. Los enlaces de carpeta de `install.sh` la conservan; copiar una skill por separado requiere trasladar también sus referencias. Cada skill lleva su licencia MIT y `references/` conserva otra copia para distribuir esos documentos.

Las skills fuera del grupo principal siguen como importadas, sin promesa de portabilidad auditada. Algunas nombran herramientas de Claude, exigen subagentes o dependen del setup de Matt Pocock. Migra una cuando la vayas a usar: conserva el comportamiento útil, elimina dependencias implícitas y prueba la nueva versión.

`.skill-lock.json` registra instalaciones de terceros, no es un manifiesto de esta colección personal. Sus hashes reflejan el contenido importado, no las modificaciones propias. Evita actualizar automáticamente `code-review` desde su origen: ahora es una variante local.
