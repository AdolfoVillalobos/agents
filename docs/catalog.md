# Catálogo

## Flujo principal

| Skill | Cuándo usarla | Estado y procedencia |
| --- | --- | --- |
| [code-review](../skills/code-review/SKILL.md) | Buscar fallas y contrastar cada hallazgo con evidencia | Draft propio; adaptado del review por standards/spec de `mattpocock/skills` |
| [diff-minimality](../skills/diff-minimality/SKILL.md) | Simplificar preservando comportamiento | Draft local existente, separado del flujo de publicación |
| [create-pr](../skills/create-pr/SKILL.md) | Crear un PR draft autoasignado, con descripción breve en español y aprobación del texto | Draft basado en la versión Fintoc aportada por el usuario y el estudio de 50 PRs de `npcastro`; referencias y casos de evaluación adjuntos |

Estas tres usan instrucciones independientes del proveedor. `create-pr` incluye una referencia de Fintoc con convenciones y ejemplos de redacción. Su estructura fue revisada; su comportamiento todavía debe compararse en tareas reales con cada agente.

El draft `review-pr` de `~/Documents/fintoc/claude-config/skills/review-pr` aportó contexto para la revisión: intención antes del código, lectura fuera del diff y comentarios respetuosos. Sigue en su instalación original; la versión mantenida aquí se llama `code-review`.

## Colección importada

Los grupos son navegación, no nuevos directorios ni orden obligatorio de ejecución. **Estado común: importada, pendiente de revisión de portabilidad.**

### Siempre activa

| Skill | Uso | Procedencia |
| --- | --- | --- |
| [i-have-adhd](../skills/i-have-adhd/SKILL.md) | Respuestas que empiezan por la acción y respetan el alcance de cada pregunta; recordatorio por turno en Claude | Adaptación local de [`ayghri/i-have-adhd`](https://github.com/ayghri/i-have-adhd) en `839872f`; conserva licencia MIT en `LICENSE.txt` |

[RTK](https://github.com/rtk-ai/rtk) acompaña a esta colección, pero no es una skill: es un binario con hooks propios que `install.sh` instala y configura.

### Diseño y definición

| Skill | Uso |
| --- | --- |
| [codebase-design](../skills/codebase-design/SKILL.md) | Interfaces y límites de módulos |
| [domain-modeling](../skills/domain-modeling/SKILL.md) | Vocabulario de dominio y ADRs |
| [improve-codebase-architecture](../skills/improve-codebase-architecture/SKILL.md) | Diagnóstico arquitectónico |
| [prototype](../skills/prototype/SKILL.md) | Prototipos para responder una pregunta |
| [to-spec](../skills/to-spec/SKILL.md) | Formalizar requisitos |

### Preguntas y decisiones

| Skill | Uso |
| --- | --- |
| [grilling](../skills/grilling/SKILL.md) | Cuestionar un plan mediante entrevista |
| [grill-me](../skills/grill-me/SKILL.md) | Otro flujo de entrevista; solapamiento pendiente de resolver |
| [grill-with-docs](../skills/grill-with-docs/SKILL.md) | Entrevista con documentación |
| [to-questionnaire](../skills/to-questionnaire/SKILL.md) | Preguntas para stakeholders |
| [ask-matt](../skills/ask-matt/SKILL.md) | Consultar el workflow importado |

### Implementación y diagnóstico

| Skill | Uso |
| --- | --- |
| [implement](../skills/implement/SKILL.md) | Ejecutar una especificación |
| [tdd](../skills/tdd/SKILL.md) | Desarrollo guiado por tests |
| [diagnosing-bugs](../skills/diagnosing-bugs/SKILL.md) | Diagnóstico de bugs |
| [resolving-merge-conflicts](../skills/resolving-merge-conflicts/SKILL.md) | Resolver conflictos por intención |
| [vercel-composition-patterns](../skills/vercel-composition-patterns/SKILL.md) | Composición de componentes React |

### Coordinación del trabajo

| Skill | Uso |
| --- | --- |
| [to-tickets](../skills/to-tickets/SKILL.md) | Descomponer una spec en tickets |
| [triage](../skills/triage/SKILL.md) | Preparar reportes externos |
| [wayfinder](../skills/wayfinder/SKILL.md) | Navegar proyectos largos |
| [handoff](../skills/handoff/SKILL.md) | Transferir contexto entre sesiones |
| [wizard](../skills/wizard/SKILL.md) | Guiar pasos manuales |

### Investigación, aprendizaje y escritura

| Skill | Uso |
| --- | --- |
| [research](../skills/research/SKILL.md) | Investigar con fuentes primarias |
| [teach](../skills/teach/SKILL.md) | Aprender en el workspace |
| [wait-what](../skills/wait-what/SKILL.md) | Explicar de otra manera |
| [writing-guidelines](../skills/writing-guidelines/SKILL.md) | Revisar prosa |
| [web-design-guidelines](../skills/web-design-guidelines/SKILL.md) | Revisar interfaces |

### Mantenimiento de skills

| Skill | Uso |
| --- | --- |
| [writing-for-agents](../skills/writing-for-agents/SKILL.md) | Redactar instrucciones para agentes |
| [skill-creator](../skills/skill-creator/SKILL.md) | Crear y evaluar skills; contiene integración específica de Claude |
| [find-skills](../skills/find-skills/SKILL.md) | Descubrir skills de terceros |
| [setup-matt-pocock-skills](../skills/setup-matt-pocock-skills/SKILL.md) | Configurar el workflow importado |

## Procedencia

La colección inicial contiene 31 skills; `create-pr` lleva el total a 32 e `i-have-adhd` a 33. `.skill-lock.json` conserva repositorios y hashes de la instalación original:

- `mattpocock/skills`: colección de ingeniería, incluida la base original de `code-review`.
- `vercel-labs/agent-skills`: composición React, guidelines de diseño y escritura.
- `vercel-labs/skills`: `find-skills`.
- `anthropics/skills`: `skill-creator`; conserva su licencia incluida.

`diff-minimality` no tenía entrada de origen en el lock. Las adaptaciones locales no se actualizan automáticamente desde sus fuentes. Mantén licencias y atribuciones originales cuando traslades una carpeta.
