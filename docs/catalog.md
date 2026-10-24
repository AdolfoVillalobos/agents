# Catálogo

## Flujo principal

| Skill | Cuándo usarla | Estado y procedencia |
| --- | --- | --- |
| [code-review](../skills/code-review/SKILL.md) | Buscar fallas y contrastar cada hallazgo con evidencia | Draft propio; adaptado del review por standards/spec de `mattpocock/skills` |
| [diff-minimality](../skills/diff-minimality/SKILL.md) | Simplificar preservando comportamiento | Draft local existente, separado del flujo de publicación |
| [create-pr](../skills/create-pr/SKILL.md) | Crear un PR draft autoasignado, con título en inglés, descripción breve en español y primera persona cuando corresponde | Draft basado en la versión Fintoc aportada por el usuario y el estudio de 50 PRs de `npcastro`; referencias y casos de evaluación adjuntos |

Estas tres usan instrucciones independientes del proveedor. `create-pr` incluye una referencia de Fintoc con convenciones y ejemplos de redacción. Su estructura fue revisada; su comportamiento todavía debe compararse en tareas reales con cada agente.

## Revisiones especializadas

| Skill | Cuándo usarla | Estado y procedencia |
| --- | --- | --- |
| [review-design](../skills/review-design/SKILL.md) | Revisar límites, estructura y oportunidades de simplificación de un diff | Draft propio a partir del prompt A aportado por el usuario |
| [review-qa](../skills/review-qa/SKILL.md) | Buscar regresiones recorriendo flujos y ejecutando comprobaciones focalizadas | Draft propio a partir del prompt B aportado por el usuario |
| [review-readiness](../skills/review-readiness/SKILL.md) | Evaluar intención, despliegue, compatibilidad y preparación para merge | Draft propio a partir del prompt C aportado por el usuario |
| [review-comments](../skills/review-comments/SKILL.md) | Convertir un review ya hecho en comentarios anclados, listos para pegar | Draft propio a partir del paquete `pr-review-assist` y el brief de comentarios aportados el 2026-10-13 |

`review-design`, `review-qa` y `review-readiness` son alternativas para pedir un pase específico. `code-review` conserva la revisión general. `review-comments` formatea los hallazgos que sobrevivieron. Si todavía no hay informe, corre antes el pase que corresponda. Comparten [protocolo y rúbrica](../skills/code-review/references/review-protocol.md), con una [referencia de pagos](../skills/code-review/references/payment-invariants.md) que se lee solo cuando aplica. [Procedencia, adaptaciones y casos de evaluación](review-skills.md). Validación estructural; evaluación con modelos pendiente.

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

### Colección de Addy Osmani

Las 25 skills de [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills) se importaron desde [`aeac41d`](https://github.com/addyosmani/agent-skills/commit/aeac41d4d005999432bb7312f7ff06383a91d59d). Conservan sus nombres, instrucciones y recursos originales; cada carpeta incluye la licencia MIT de Addy Osmani. Estado: **importadas, sin auditoría de comportamiento ni portabilidad completa**. Las referencias compartidas viven en [`references/`](../references/); conserva esa carpeta junto a `skills/` al trasladarlas. [Instalación, alcance y comprobaciones](addyosmani-agent-skills.md).

| Skill | Uso |
| --- | --- |
| [using-agent-skills](../skills/using-agent-skills/SKILL.md) | Descubrir el flujo adecuado de esta colección |
| [interview-me](../skills/interview-me/SKILL.md) | Aclarar requisitos con preguntas |
| [idea-refine](../skills/idea-refine/SKILL.md) | Refinar y contrastar ideas |
| [spec-driven-development](../skills/spec-driven-development/SKILL.md) | Definir una especificación antes de implementar |
| [planning-and-task-breakdown](../skills/planning-and-task-breakdown/SKILL.md) | Dividir una especificación en tareas |
| [incremental-implementation](../skills/incremental-implementation/SKILL.md) | Implementar por incrementos verificables |
| [test-driven-development](../skills/test-driven-development/SKILL.md) | Trabajar con el ciclo red-green-refactor |
| [debugging-and-error-recovery](../skills/debugging-and-error-recovery/SKILL.md) | Diagnosticar fallas y recuperar el flujo |
| [code-review-and-quality](../skills/code-review-and-quality/SKILL.md) | Revisar corrección, claridad, arquitectura, seguridad y rendimiento |
| [code-simplification](../skills/code-simplification/SKILL.md) | Simplificar preservando comportamiento |
| [doubt-driven-development](../skills/doubt-driven-development/SKILL.md) | Contrastar decisiones mediante una revisión adversarial independiente |
| [constraint-driven-development](../skills/constraint-driven-development/SKILL.md) | Definir y comprobar el estándar de calidad del proyecto |
| [frontend-ui-engineering](../skills/frontend-ui-engineering/SKILL.md) | Construir interfaces accesibles y adaptables |
| [api-and-interface-design](../skills/api-and-interface-design/SKILL.md) | Diseñar contratos de API e interfaces |
| [browser-testing-with-devtools](../skills/browser-testing-with-devtools/SKILL.md) | Verificar interfaces mediante Chrome DevTools MCP |
| [performance-optimization](../skills/performance-optimization/SKILL.md) | Medir y mejorar rendimiento |
| [security-and-hardening](../skills/security-and-hardening/SKILL.md) | Revisar y reforzar seguridad |
| [observability-and-instrumentation](../skills/observability-and-instrumentation/SKILL.md) | Diseñar logs, métricas y alertas |
| [git-workflow-and-versioning](../skills/git-workflow-and-versioning/SKILL.md) | Gestionar ramas, commits y versiones |
| [ci-cd-and-automation](../skills/ci-cd-and-automation/SKILL.md) | Configurar automatización y pipelines |
| [shipping-and-launch](../skills/shipping-and-launch/SKILL.md) | Preparar despliegues y lanzamientos |
| [deprecation-and-migration](../skills/deprecation-and-migration/SKILL.md) | Migrar y retirar sistemas con compatibilidad |
| [context-engineering](../skills/context-engineering/SKILL.md) | Preparar el contexto de trabajo del agente |
| [source-driven-development](../skills/source-driven-development/SKILL.md) | Verificar decisiones contra documentación primaria |
| [documentation-and-adrs](../skills/documentation-and-adrs/SKILL.md) | Escribir documentación y decisiones de arquitectura |

Las skills propias del flujo principal mantienen su lugar. Las importadas ofrecen otros procesos con nombres distintos; no sustituyen `code-review`, `tdd`, `diff-minimality` ni las revisiones especializadas.

## Procedencia

La colección inicial contiene 31 skills; `create-pr` lleva el total a 32, `i-have-adhd` a 33, las tres revisiones especializadas a 36, `review-comments` a 37 y las 25 de Addy Osmani a 62. `.skill-lock.json` conserva repositorios y hashes de las importaciones:

- `mattpocock/skills`: colección de ingeniería, incluida la base original de `code-review`.
- `vercel-labs/agent-skills`: composición React, guidelines de diseño y escritura.
- `vercel-labs/skills`: `find-skills`.
- `anthropics/skills`: `skill-creator`; conserva su licencia incluida.
- `addyosmani/agent-skills`: 25 skills de ingeniería; `sourceRef` fija el commit importado y `skillFolderHash` registra el árbol Git original de cada skill, antes de añadir la copia local de la licencia.

`diff-minimality` no tenía entrada de origen en el lock. Las adaptaciones locales no se actualizan automáticamente desde sus fuentes. Mantén licencias y atribuciones originales cuando traslades una carpeta.
