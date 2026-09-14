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

En esta máquina el repo ya ocupa `~/.agents`, que coincide con la ubicación personal de Codex. `~/.claude/skills` actualmente enlaza a `~/Documents/fintoc/claude-config/skills`; no apunta a esta colección. Para usar una de estas versiones en Claude ahora, dale la ruta explícita. Una instalación posterior puede enlazar cada carpeta seleccionada, revisando colisiones antes de reemplazar nada.

En Conductor, el directorio de trabajo es otra copia de Git. Invoca la ruta de ese workspace para probar un draft: una skill descubierta globalmente puede seguir leyendo la versión del checkout principal.

## Skills importadas

Las skills fuera del grupo principal siguen como importadas, sin promesa de portabilidad auditada. Algunas nombran herramientas de Claude, exigen subagentes o dependen del setup de Matt Pocock. Migra una cuando la vayas a usar: conserva el comportamiento útil, elimina dependencias implícitas y prueba la nueva versión.

`.skill-lock.json` registra instalaciones de terceros, no es un manifiesto de esta colección personal. Sus hashes reflejan el contenido importado, no las modificaciones propias. Evita actualizar automáticamente `code-review` desde su origen: ahora es una variante local.
