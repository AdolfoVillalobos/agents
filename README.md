# Skills de trabajo

Empieza por el [catálogo](docs/catalog.md). Las skills viven en `skills/<nombre>/SKILL.md`; esa carpeta es la fuente de verdad y se puede copiar completa a otro agente.

## Flujo diario

| Necesidad | Skill | Resultado |
| --- | --- | --- |
| Cuestionar una implementación | [code-review](skills/code-review/SKILL.md) | Hallazgos con evidencia y contraargumentos comprobados |
| Reducir complejidad | [diff-minimality](skills/diff-minimality/SKILL.md) | Cambios más simples que preservan comportamiento |
| Preparar un PR entendible | [create-pr](skills/create-pr/SKILL.md) | Título, descripción y validación basados en el diff final |
| Dejar comentarios para pegar | [review-comments](skills/review-comments/SKILL.md) | Borradores anclados a la línea, a partir de un review ya hecho |

Estas skills son drafts propios para iterar. El resto del catálogo conserva las skills importadas y su estado de portabilidad pendiente.

También incluye las [25 skills de Addy Osmani](docs/addyosmani-agent-skills.md), con sus referencias compartidas y licencia MIT, disponibles mediante la misma instalación.

## Organización

```text
skills/<nombre>/
  SKILL.md              # instrucciones y cuándo usarlas
  references/           # material opcional, cuando haga falta
  scripts/              # automatización propia de la skill
  agents/openai.yaml    # metadatos opcionales de Codex, si existen
hooks/                  # hooks que install.sh registra
install.sh              # instalación para Claude Code y Codex
Makefile                # atajos para install.sh
docs/
  catalog.md            # mapa por uso, procedencia y estado
  workflow.md           # iteración en Conductor
  portability.md        # carga en distintos agentes
AGENTS.md               # instrucciones para editar este repositorio
CLAUDE.md               # entrada a esas mismas instrucciones
```

Las categorías viven en el catálogo: mantener un nivel de carpetas evita cambiar rutas e instalaciones al reorganizar por tema. Los ejemplos de ejecución se escriben en lenguaje natural; los atajos de cada agente quedan en [portabilidad](docs/portability.md).

## Iterar

1. Abre el repo en Conductor siguiendo [el flujo de trabajo](docs/workflow.md).
2. Edita una skill por cambio y prueba su comportamiento con una tarea representativa.
3. Conserva una comparación antes/después; incorpora la versión elegida a la rama principal.

## Instalar

```bash
make install   # make sin argumentos lista las variantes
```

Enlaza las skills para Claude Code y Codex, deja `i-have-adhd` siempre activo e instala [RTK](https://github.com/rtk-ai/rtk) con sus hooks. Opciones y detalles en [portabilidad](docs/portability.md#instalación). Los hooks propios viven en `hooks/`; el resto de la ejecución automática pertenece a la integración de cada herramienta.
