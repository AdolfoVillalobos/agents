# Catálogo

Cada nombre público incluye el módulo que mantiene la skill. El nombre interno de `SKILL.md` se conserva.

| Módulo | Skills | Criterio |
| --- | --- | --- |
| `personal` | 8 | Propias y adaptadas localmente |
| `matt-pocock` | 24 | Importadas de Matt Pocock |
| `addyosmani` | 25 | Importadas de Addy Osmani |
| `vercel` | 4 | Importadas de Vercel |
| `anthropic` | 1 | Importada de Anthropic |

[Instalación por módulos](portability.md#instalación).

## Flujo principal

| Skill | Cuándo usarla | Estado y procedencia |
| --- | --- | --- |
| [personal:code-review](../modules/personal/skills/code-review/SKILL.md) | Buscar fallas y contrastar cada hallazgo con evidencia | Draft propio; adaptado del review por standards/spec de `mattpocock/skills` |
| [personal:diff-minimality](../modules/personal/skills/diff-minimality/SKILL.md) | Simplificar preservando comportamiento | Draft local existente, separado del flujo de publicación |
| [personal:create-pr](../modules/personal/skills/create-pr/SKILL.md) | Crear un PR draft autoasignado, con título en inglés, descripción breve en español y primera persona cuando corresponde | Draft basado en la versión Fintoc aportada por el usuario y el estudio de 50 PRs de `npcastro`; referencias y casos de evaluación adjuntos |

Estas tres usan instrucciones independientes del proveedor. `create-pr` incluye una referencia de Fintoc con convenciones y ejemplos de redacción. Su estructura fue revisada; su comportamiento todavía debe compararse en tareas reales con cada agente.

## Revisiones especializadas

| Skill | Cuándo usarla | Estado y procedencia |
| --- | --- | --- |
| [personal:review-design](../modules/personal/skills/review-design/SKILL.md) | Revisar límites, estructura y oportunidades de simplificación de un diff | Draft propio a partir del prompt A aportado por el usuario |
| [personal:review-qa](../modules/personal/skills/review-qa/SKILL.md) | Buscar regresiones recorriendo flujos y ejecutando comprobaciones focalizadas | Draft propio a partir del prompt B aportado por el usuario |
| [personal:review-readiness](../modules/personal/skills/review-readiness/SKILL.md) | Evaluar intención, despliegue, compatibilidad y preparación para merge | Draft propio a partir del prompt C aportado por el usuario |
| [personal:review-comments](../modules/personal/skills/review-comments/SKILL.md) | Convertir un review ya hecho en comentarios anclados, listos para pegar | Draft propio a partir del paquete `pr-review-assist` y el brief de comentarios aportados el 2026-10-13 |

`review-design`, `review-qa` y `review-readiness` son alternativas para pedir un pase específico. `code-review` conserva la revisión general. `review-comments` formatea los hallazgos que sobrevivieron. Si todavía no hay informe, corre antes el pase que corresponda. Comparten [protocolo y rúbrica](../modules/personal/skills/code-review/references/review-protocol.md), con una [referencia de pagos](../modules/personal/skills/code-review/references/payment-invariants.md) que se lee solo cuando aplica. [Procedencia, adaptaciones y casos de evaluación](review-skills.md). Validación estructural; evaluación con modelos pendiente.

El draft `review-pr` de `~/Documents/fintoc/claude-config/skills/review-pr` aportó contexto para la revisión: intención antes del código, lectura fuera del diff y comentarios respetuosos. Sigue en su instalación original; la versión mantenida aquí se llama `code-review`.

## Colección importada

Los grupos temáticos siguientes son navegación. Los directorios corresponden a módulos por mantenedor. Las importaciones siguen pendientes de revisión de portabilidad; las adaptaciones propias pertenecen a `personal` y conservan su procedencia.

### Siempre activa

| Skill | Uso | Procedencia |
| --- | --- | --- |
| [personal:i-have-adhd](../modules/personal/skills/i-have-adhd/SKILL.md) | Respuestas que empiezan por la acción y respetan el alcance de cada pregunta; recordatorio por turno en Claude | Adaptación local de [`ayghri/i-have-adhd`](https://github.com/ayghri/i-have-adhd) en `839872f`; conserva licencia MIT en `LICENSE.txt` |

[RTK](https://github.com/rtk-ai/rtk) acompaña a esta colección, pero no es una skill: es un binario con hooks propios que `install.sh` instala y configura.

### Diseño y definición

| Skill | Uso |
| --- | --- |
| [matt-pocock:codebase-design](../modules/matt-pocock/skills/codebase-design/SKILL.md) | Interfaces y límites de módulos |
| [matt-pocock:domain-modeling](../modules/matt-pocock/skills/domain-modeling/SKILL.md) | Vocabulario de dominio y ADRs |
| [matt-pocock:improve-codebase-architecture](../modules/matt-pocock/skills/improve-codebase-architecture/SKILL.md) | Diagnóstico arquitectónico |
| [matt-pocock:prototype](../modules/matt-pocock/skills/prototype/SKILL.md) | Prototipos para responder una pregunta |
| [matt-pocock:to-spec](../modules/matt-pocock/skills/to-spec/SKILL.md) | Formalizar requisitos |

### Preguntas y decisiones

| Skill | Uso |
| --- | --- |
| [matt-pocock:grilling](../modules/matt-pocock/skills/grilling/SKILL.md) | Cuestionar un plan mediante entrevista |
| [matt-pocock:grill-me](../modules/matt-pocock/skills/grill-me/SKILL.md) | Otro flujo de entrevista; solapamiento pendiente de resolver |
| [matt-pocock:grill-with-docs](../modules/matt-pocock/skills/grill-with-docs/SKILL.md) | Entrevista con documentación |
| [matt-pocock:to-questionnaire](../modules/matt-pocock/skills/to-questionnaire/SKILL.md) | Preguntas para stakeholders |
| [matt-pocock:ask-matt](../modules/matt-pocock/skills/ask-matt/SKILL.md) | Consultar el workflow importado |

### Implementación y diagnóstico

| Skill | Uso |
| --- | --- |
| [matt-pocock:implement](../modules/matt-pocock/skills/implement/SKILL.md) | Ejecutar una especificación |
| [matt-pocock:tdd](../modules/matt-pocock/skills/tdd/SKILL.md) | Desarrollo guiado por tests |
| [matt-pocock:diagnosing-bugs](../modules/matt-pocock/skills/diagnosing-bugs/SKILL.md) | Diagnóstico de bugs |
| [matt-pocock:resolving-merge-conflicts](../modules/matt-pocock/skills/resolving-merge-conflicts/SKILL.md) | Resolver conflictos por intención |
| [vercel:vercel-composition-patterns](../modules/vercel/skills/vercel-composition-patterns/SKILL.md) | Composición de componentes React |

### Coordinación del trabajo

| Skill | Uso |
| --- | --- |
| [matt-pocock:to-tickets](../modules/matt-pocock/skills/to-tickets/SKILL.md) | Descomponer una spec en tickets |
| [matt-pocock:triage](../modules/matt-pocock/skills/triage/SKILL.md) | Preparar reportes externos |
| [matt-pocock:wayfinder](../modules/matt-pocock/skills/wayfinder/SKILL.md) | Navegar proyectos largos |
| [matt-pocock:handoff](../modules/matt-pocock/skills/handoff/SKILL.md) | Transferir contexto entre sesiones |
| [matt-pocock:wizard](../modules/matt-pocock/skills/wizard/SKILL.md) | Guiar pasos manuales |

### Investigación, aprendizaje y escritura

| Skill | Uso |
| --- | --- |
| [matt-pocock:research](../modules/matt-pocock/skills/research/SKILL.md) | Investigar con fuentes primarias |
| [matt-pocock:teach](../modules/matt-pocock/skills/teach/SKILL.md) | Aprender en el workspace |
| [matt-pocock:wait-what](../modules/matt-pocock/skills/wait-what/SKILL.md) | Explicar de otra manera |
| [vercel:writing-guidelines](../modules/vercel/skills/writing-guidelines/SKILL.md) | Revisar prosa |
| [vercel:web-design-guidelines](../modules/vercel/skills/web-design-guidelines/SKILL.md) | Revisar interfaces |

### Mantenimiento de skills

| Skill | Uso |
| --- | --- |
| [matt-pocock:writing-for-agents](../modules/matt-pocock/skills/writing-for-agents/SKILL.md) | Redactar instrucciones para agentes |
| [anthropic:skill-creator](../modules/anthropic/skills/skill-creator/SKILL.md) | Crear y evaluar skills; contiene integración específica de Claude |
| [vercel:find-skills](../modules/vercel/skills/find-skills/SKILL.md) | Descubrir skills de terceros |
| [matt-pocock:setup-matt-pocock-skills](../modules/matt-pocock/skills/setup-matt-pocock-skills/SKILL.md) | Configurar el workflow importado |

### Colección de Addy Osmani

Las 25 skills de [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills) se importaron desde [`aeac41d`](https://github.com/addyosmani/agent-skills/commit/aeac41d4d005999432bb7312f7ff06383a91d59d). Conservan sus nombres, instrucciones y recursos originales; cada carpeta incluye la licencia MIT de Addy Osmani. Estado: **importadas, sin auditoría de comportamiento ni portabilidad completa**. Las referencias compartidas viven en [`modules/addyosmani/references/`](../modules/addyosmani/references/); traslada el módulo `addyosmani` completo. [Instalación, alcance y comprobaciones](addyosmani-agent-skills.md).

| Skill | Uso |
| --- | --- |
| [addyosmani:using-agent-skills](../modules/addyosmani/skills/using-agent-skills/SKILL.md) | Descubrir el flujo adecuado de esta colección |
| [addyosmani:interview-me](../modules/addyosmani/skills/interview-me/SKILL.md) | Aclarar requisitos con preguntas |
| [addyosmani:idea-refine](../modules/addyosmani/skills/idea-refine/SKILL.md) | Refinar y contrastar ideas |
| [addyosmani:spec-driven-development](../modules/addyosmani/skills/spec-driven-development/SKILL.md) | Definir una especificación antes de implementar |
| [addyosmani:planning-and-task-breakdown](../modules/addyosmani/skills/planning-and-task-breakdown/SKILL.md) | Dividir una especificación en tareas |
| [addyosmani:incremental-implementation](../modules/addyosmani/skills/incremental-implementation/SKILL.md) | Implementar por incrementos verificables |
| [addyosmani:test-driven-development](../modules/addyosmani/skills/test-driven-development/SKILL.md) | Trabajar con el ciclo red-green-refactor |
| [addyosmani:debugging-and-error-recovery](../modules/addyosmani/skills/debugging-and-error-recovery/SKILL.md) | Diagnosticar fallas y recuperar el flujo |
| [addyosmani:code-review-and-quality](../modules/addyosmani/skills/code-review-and-quality/SKILL.md) | Revisar corrección, claridad, arquitectura, seguridad y rendimiento |
| [addyosmani:code-simplification](../modules/addyosmani/skills/code-simplification/SKILL.md) | Simplificar preservando comportamiento |
| [addyosmani:doubt-driven-development](../modules/addyosmani/skills/doubt-driven-development/SKILL.md) | Contrastar decisiones mediante una revisión adversarial independiente |
| [addyosmani:constraint-driven-development](../modules/addyosmani/skills/constraint-driven-development/SKILL.md) | Definir y comprobar el estándar de calidad del proyecto |
| [addyosmani:frontend-ui-engineering](../modules/addyosmani/skills/frontend-ui-engineering/SKILL.md) | Construir interfaces accesibles y adaptables |
| [addyosmani:api-and-interface-design](../modules/addyosmani/skills/api-and-interface-design/SKILL.md) | Diseñar contratos de API e interfaces |
| [addyosmani:browser-testing-with-devtools](../modules/addyosmani/skills/browser-testing-with-devtools/SKILL.md) | Verificar interfaces mediante Chrome DevTools MCP |
| [addyosmani:performance-optimization](../modules/addyosmani/skills/performance-optimization/SKILL.md) | Medir y mejorar rendimiento |
| [addyosmani:security-and-hardening](../modules/addyosmani/skills/security-and-hardening/SKILL.md) | Revisar y reforzar seguridad |
| [addyosmani:observability-and-instrumentation](../modules/addyosmani/skills/observability-and-instrumentation/SKILL.md) | Diseñar logs, métricas y alertas |
| [addyosmani:git-workflow-and-versioning](../modules/addyosmani/skills/git-workflow-and-versioning/SKILL.md) | Gestionar ramas, commits y versiones |
| [addyosmani:ci-cd-and-automation](../modules/addyosmani/skills/ci-cd-and-automation/SKILL.md) | Configurar automatización y pipelines |
| [addyosmani:shipping-and-launch](../modules/addyosmani/skills/shipping-and-launch/SKILL.md) | Preparar despliegues y lanzamientos |
| [addyosmani:deprecation-and-migration](../modules/addyosmani/skills/deprecation-and-migration/SKILL.md) | Migrar y retirar sistemas con compatibilidad |
| [addyosmani:context-engineering](../modules/addyosmani/skills/context-engineering/SKILL.md) | Preparar el contexto de trabajo del agente |
| [addyosmani:source-driven-development](../modules/addyosmani/skills/source-driven-development/SKILL.md) | Verificar decisiones contra documentación primaria |
| [addyosmani:documentation-and-adrs](../modules/addyosmani/skills/documentation-and-adrs/SKILL.md) | Escribir documentación y decisiones de arquitectura |

Las skills propias del flujo principal mantienen su lugar. Las importadas ofrecen otros procesos con nombres distintos; no sustituyen `code-review`, `tdd`, `diff-minimality` ni las revisiones especializadas.

## Procedencia

La colección inicial contiene 31 skills; `create-pr` lleva el total a 32, `i-have-adhd` a 33, las tres revisiones especializadas a 36, `review-comments` a 37 y las 25 de Addy Osmani a 62. `.skill-lock.json` usa nombres cualificados y conserva origen, ruta original y ruta local de las importaciones:

- `mattpocock/skills`: colección de ingeniería, incluida la base original de `code-review`.
- `vercel-labs/agent-skills`: composición React, guidelines de diseño y escritura.
- `vercel-labs/skills`: `find-skills`.
- `anthropics/skills`: `skill-creator`; conserva su licencia incluida.
- `addyosmani/agent-skills`: 25 skills de ingeniería; `sourceRef` fija el commit importado y `skillFolderHash` registra el árbol Git original de cada skill, antes de añadir la copia local de la licencia.

`diff-minimality` no tenía entrada de origen en el lock. Las adaptaciones locales no se actualizan automáticamente desde sus fuentes. Mantén licencias y atribuciones originales cuando traslades una carpeta.
