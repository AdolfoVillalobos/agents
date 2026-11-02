# Skills de trabajo

Instala la colección con `make install` desde el checkout principal. Las skills se agrupan por mantenedor y se invocan con nombres como `personal:code-review`, `matt-pocock:tdd` o `addyosmani:spec-driven-development`.

## Flujo diario

| Necesidad | Skill |
| --- | --- |
| Cuestionar una implementación | [personal:code-review](modules/personal/skills/code-review/SKILL.md) |
| Reducir complejidad | [personal:diff-minimality](modules/personal/skills/diff-minimality/SKILL.md) |
| Preparar un PR entendible | [personal:create-pr](modules/personal/skills/create-pr/SKILL.md) |
| Dejar comentarios para pegar | [personal:review-comments](modules/personal/skills/review-comments/SKILL.md) |

El [catálogo](docs/catalog.md) reúne las 63 skills de `personal`, `matt-pocock`, `addyosmani`, `vercel`, `anthropic` y `humanlayer`. Las propias y adaptadas viven en `personal`; cada importación conserva su atribución y licencia incluida.

## Organización

```text
modules/<módulo>/
  plugin.json                 # identidad del módulo y manifest portable
  .claude-plugin/plugin.json  # adaptador de Claude Code
  skills/<nombre>/SKILL.md    # única fuente de comportamiento
  references/                 # recursos compartidos del módulo, si existen
.agents/plugins/marketplace.json  # catálogo para Codex
.claude-plugin/marketplace.json   # catálogo para Claude Code
scripts/install_modules.py    # registro nativo y migración de accesos antiguos
hooks/                        # recordatorios de personal:i-have-adhd
install.sh                    # instalación, ADHD y RTK
```

El prefijo lo aporta el plugin. Los `name` de las skills conservan su valor original y las referencias de cada módulo viajan juntas. El [glosario](CONTEXT.md) distingue módulo, nombre cualificado y procedencia.

## Instalar en otro dispositivo

1. Sincroniza el repo y abre su checkout principal, fuera de un worktree temporal.
2. Ejecuta `make install`. Usa `make install-no-rtk` para omitir RTK.
3. Abre una sesión nueva. En Claude Code, prueba `/personal:code-review`. En Codex, selecciona `personal:code-review` en el menú de skills.

El instalador registra los módulos en los clientes disponibles. Requiere Python 3 y `jq`, además del CLI de Codex o Claude Code con soporte de plugins. Respalda los accesos antiguos reconocidos y conserva las skills ajenas. [Opciones, migración y recursos](docs/portability.md).

## Iterar

1. Abre el repo en Conductor siguiendo [el flujo de trabajo](docs/workflow.md).
2. Edita la skill del módulo correspondiente y prueba una tarea representativa.
3. Compara el comportamiento y publica la versión elegida.
