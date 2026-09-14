# Skills de trabajo

Empieza por el [catálogo](docs/catalog.md). Las skills viven en `skills/<nombre>/SKILL.md`; esa carpeta es la fuente de verdad y se puede copiar completa a otro agente.

## Flujo diario

| Necesidad | Skill | Resultado |
| --- | --- | --- |
| Cuestionar una implementación | [code-review](skills/code-review/SKILL.md) | Hallazgos con evidencia y contraargumentos comprobados |
| Reducir complejidad | [diff-minimality](skills/diff-minimality/SKILL.md) | Cambios más simples que preservan comportamiento |
| Preparar un PR entendible | [create-pr](skills/create-pr/SKILL.md) | Título, descripción y validación basados en el diff final |

Estas tres son drafts propios para iterar. El resto del catálogo conserva las skills importadas y su estado de portabilidad pendiente.

## Organización

```text
skills/<nombre>/
  SKILL.md              # instrucciones y cuándo usarlas
  references/           # material opcional, cuando haga falta
  scripts/              # automatización propia de la skill
  agents/openai.yaml    # metadatos opcionales de Codex, si existen
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

Los hooks quedan fuera de esta primera organización. Una skill describe un procedimiento; su ejecución automática pertenece a la integración de cada herramienta.
