# Portabilidad

## Contrato común

Cada módulo se distribuye como un plugin con `skills/<nombre>/SKILL.md` y sus recursos. La fuente del repo es `modules/<módulo>/skills/<nombre>/SKILL.md`. El frontmatter conserva el `name` original; el plugin aporta el namespace público `<módulo>:<nombre>`.

`plugin.json` declara la identidad portable del módulo. `.claude-plugin/plugin.json` es su adaptador para Claude Code. `.agents/plugins/marketplace.json` y `.claude-plugin/marketplace.json` describen las mismas cinco colecciones para cada cliente. Las instrucciones necesarias viven en las skills, no en los adaptadores. `agents/openai.yaml`, cuando existe dentro de una skill, sigue siendo metadato opcional de Codex.

Agrupamos por mantenedor: las propias y adaptadas están en `personal`, y las demás en `matt-pocock`, `addyosmani`, `vercel` y `anthropic`. `.skill-lock.json` distingue el módulo actual de la procedencia original. Sus claves usan nombres cualificados; `localPath` apunta al repo y `skillPath` conserva la ruta del origen.

El namespace de plugin está documentado por [OpenAI](https://developers.openai.com/plugins/build/plugins) y [Claude Code](https://code.claude.com/docs/en/plugin-marketplaces). Cambiar el directorio o insertar dos puntos en el `name` de una skill suelta no crea esa identidad de plugin.

La identidad del plugin y la etiqueta del menú son campos distintos. En Matt Pocock, `agents/openai.yaml` declara `interface.display_name` con el nombre cualificado, por ejemplo `matt-pocock:wayfinder`; así la etiqueta también identifica la colección. Es un ajuste local de presentación del adaptador, sin cambios en los nombres internos ni en las instrucciones importadas. Addy Osmani no declara estas etiquetas personalizadas. [Referencia del campo](https://developers.openai.com/plugins/deploy/submission-errors#skill-agent-metadata-errors).

Caso de comprobación: después de reinstalar desde el checkout principal y abrir una sesión nueva, buscar `wayfinder` y `prototype` en el selector. Las entradas de este módulo deben mostrar `matt-pocock:wayfinder` y `matt-pocock:prototype`. La colección externa `matt-skills-curated` puede ofrecer otras entradas con etiquetas sin prefijo; este cambio no modifica ese plugin. La comprobación de los YAML es estructural; la verificación visual en el cliente queda pendiente.

## Usar desde cualquier agente

Invoca el nombre cualificado en el cliente o pide una ruta explícita para probar una versión concreta:

```text
Lee modules/personal/skills/code-review/SKILL.md de este checkout
para revisar el repositorio <ruta>, comparando <base> con <head>.
```

Claude Code expone `/personal:code-review`. En Codex, selecciona `personal:code-review` en el menú de skills. Otro agente puede leer el módulo completo si admite Agent Skills, aunque su mecanismo de invocación puede variar. Compatibilidad del formato no garantiza comportamiento idéntico entre modelos.

Las skills de revisión de `personal` comparten el protocolo y la rúbrica de `skills/code-review/references/` dentro de ese módulo. `review-readiness` y `review-comments` también consultan `create-pr`. Traslada el módulo completo para conservar esos recursos hermanos.

## Instalación

1. Ejecuta `make install` desde el checkout principal. Localízalo con `git worktree list`; el instalador rechaza los worktrees temporales.
2. Abre una sesión nueva del agente para cargar los módulos.

Requiere Python 3, `jq` y al menos un CLI disponible con soporte de plugins. Para Codex usa `codex plugin marketplace add` y `codex plugin add`. Para Claude Code usa `claude plugin marketplace add` y `claude plugin install`. El marketplace local se llama `work-skills`. Cada ejecución refresca los paquetes desde este checkout, sin volver a descargar las colecciones de origen.

El instalador no crea la exportación plana en `~/.agents/skills` o `~/.claude/skills`. Los clientes administran las copias instaladas en sus propios caches de plugins. Después de editar el repo, repite el instalador para refrescarlas.

### Migración de instalaciones anteriores

Después de registrar todos los módulos correctamente, mueve los accesos planos reconocidos a `~/.agents/backups/install-…`. Reconoce enlaces al antiguo `skills/` de este checkout o de otro checkout con el mismo `origin`, y los enlaces a la copia estable de Addy Osmani creada antes de los módulos. Conserva las skills ajenas, los enlaces rotos ajenos y los recursos sin seguimiento como `synced/`. Los directorios de origen permanecen intactos.

Un enlace de carpeta que pertenecía a esta colección se respalda completo. Los hijos ajenos se conservan accesibles mediante enlaces individuales. Si un cliente falla al instalar, los accesos planos siguen disponibles. Los registros nativos ya aceptados y la configuración preparada pueden haber cambiado; corrige la falla y repite el instalador. No hay una transacción común entre los dos clientes.

Si ya existe otro marketplace `work-skills` con un origen distinto, el instalador se detiene antes de cambiar la configuración. No sustituye ese registro ni sus plugins. Si corresponde a otro checkout con el mismo `origin`, respalda los registros y vuelve a registrar la colección desde el checkout actual.

### ADHD y RTK

`personal:i-have-adhd` conserva el modo siempre activo: Claude carga las reglas con `SessionStart` y un recordatorio breve con `UserPromptSubmit`; Codex recibe el bloque delimitado en su `AGENTS.md`. Los hooks leen la skill en `modules/personal/skills/i-have-adhd/`. En una sesión, «stop adhd mode» lo desactiva.

`make adhd-on-demand` retira los hooks ADHD conocidos y el bloque de Codex. La skill continúa disponible por su nombre cualificado. `make install-no-rtk` omite la instalación y configuración de RTK. Los cambios en el contenido copiado al `AGENTS.md` de Codex requieren repetir el instalador.

Antes de escribir, el instalador respalda la configuración. Conserva otros ajustes y hooks, incluidos los de RTK. Migra invocaciones simples de los scripts ADHD, incluso con comillas o mediante `sh` o `bash`. Si un hook combina ADHD con otros comandos, se detiene sin modificar la configuración: separa la invocación ADHD. También rechaza JSON inválido y bloques incompletos de Codex antes de escribir.

La bandera `~/.claude/.i-have-adhd-always` del plugin anterior se mueve al respaldo; el plugin permanece instalado. Esto evita inyecciones duplicadas. El recordatorio se extrae de `Turn reminder` en cada mensaje y no reactiva un modo desactivado. Que se cargue una instrucción no garantiza que el modelo la siga; revisa también los [casos de evaluación](../modules/personal/skills/i-have-adhd/evaluacion.md).

### Validación aislada

`make test-install` usa configuraciones y repos temporales con dobles de los CLI. Verifica registro, reinstalación, respaldos, conservación de recursos ajenos, rechazo de configuración inválida y fallas parciales. `AGENT_INSTALL_ROOT` redirige las carpetas de configuración y exige `--skip-rtk`. No modifica `HOME`, no instala RTK ni ejecuta modelos.

La validación con los CLI reales se realiza por separado: manifests aceptados, paquetes instalados e inventario de skills. No equivale a evaluar los workflows con modelos. En Conductor, usa una ruta de este workspace para probar un draft; el cache global puede contener otra revisión.

## Review en GitHub

El workflow usa la skill `personal:code-review` fijada a la revisión base del PR, nunca las instrucciones modificadas por el propio PR. Busca primero `modules/personal/skills/code-review/SKILL.md` y recurre a la antigua `skills/code-review/SKILL.md` cuando la base todavía no contiene la migración. Las pasadas son secuenciales y un job posterior publica el resultado en español. Requiere `OPENAI_API_KEY`.

## Skills importadas

El módulo [addyosmani](addyosmani-agent-skills.md) contiene sus 25 skills y los siete documentos compartidos en `references/` dentro del paquete. Sus rutas `../../references/…` siguen resolviéndose sin modificar los originales. Cada skill y la carpeta compartida conservan la licencia MIT incluida.

Las demás importaciones mantienen su estado de portabilidad pendiente: algunas nombran herramientas o rutas específicas, exigen subagentes o dependen de un setup externo. Migra una cuando la vayas a usar, conserva el comportamiento útil y prueba la adaptación bajo `personal`. Mantén la atribución original.

Los hashes del lock reflejan las importaciones originales, no las adaptaciones. No actualizan automáticamente ninguna variante local.
