# Estado del arte: detectar y quitar "AI slop" en código de agentes (noviembre 2026)

**Fecha de la investigación:** 22 de noviembre de 2026 (America/Santiago).  
**Para:** Adolfo Villalobos, ingeniería en Fintoc. Objetivo: una skill reutilizable (`SKILL.md`) para Claude Code (`.claude/skills/`) y Codex (`.agents/skills/`), usada desde worktrees de Conductor.  
**Método:** esta investigación se hizo con búsqueda y fetch en vivo (páginas oficiales, arXiv, GitHub API, HTML de papers). No se inventan métricas ni citas. Donde la fuente es correlacional, o el PDF completo está detrás de un formulario, se dice.

**Cómo leer las cifras.** GitClear mide *líneas cambiadas en repos grandes* y correlaciona esas señales con la era de los asistentes; no prueba causalidad. El paper de Popescu et al. (2026) mide *churn y supervivencia post-merge* en PRs de agentes, con otra definición. No se pueden intercambiar. Un número que circula mucho —«el 40 % del código de AI se revierte en dos semanas, según GitClear»— **no aparece** en sus reportes ([Biggerstaff, 10 ago 2026](https://www.mikebiggerstaff.me/writing/gitclear-40-percent)).

---

## Resumen ejecutivo

El slop de agentes no es solo estilo feo. La evidencia de 2025–2026 apunta a un patrón estructural: los flujos por defecto premian un camino feliz, un test que pasa y un ticket cerrado, y postergan reuso, consolidación y exposición de errores. GitClear, sobre 623 millones de cambios (2023–2026 YTD), reporta duplicación de bloques +81 %, copy/paste intra-commit en 15,7 % de las líneas (frente a 9,4 % en 2022), código *moved*/refactor en 3,8 % (frente a 21 % en 2022), conectividad entre funciones −35 %, constructs que enmascaran errores +47 %, y churn a dos semanas +15 % ([GitClear, *The Maintainability Gap*, 2026](https://www.gitclear.com/the_ai_code_quality_maintainability_gap)).

Eso encaja con una taxonomía práctica: helpers reinventados, código muerto, sobre-abstracción y fallbacks especulativos, ruido defensivo (try/catch y null checks de más), comentarios que narran el *qué*, patrones inconsistentes con el archivo, bugs silenciosos, y tests que no fallan nunca (tests vacíos, asserts tautológicos, «verification theater»).

El estado del arte de *remoción* todavía es joven y está fragmentado:

- Anthropic ya trata la limpieza como un paso distinto del review de bugs: el plugin oficial `code-simplifier` (ene 2026) y la skill embebida `/simplify` (cuatro agentes en paralelo: reuso, simplificación, eficiencia, nivel de abstracción), siempre sobre código recién tocado y preservando comportamiento ([plugin](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-simplifier/agents/code-simplifier.md), [docs de comandos](https://code.claude.com/docs/en/commands), [tips del equipo](https://support.claude.com/en/articles/14554000-claude-code-power-user-tips)).
- Las skills open source `/deslop` y similares existen, pero casi todas tienen pocas estrellas y varias «deslop» son para prosa, no para código. La más útil como receta de limpieza de *diff* es [chrisliu298/deslop](https://github.com/chrisliu298/deslop) (1 estrella al 22 nov 2026; basada en el prompt de @lucasb-eyer). [MrZoyo/deslop-GPT](https://github.com/MrZoyo/deslop-GPT) (141 estrellas) aporta el ángulo de borrar *test bloat*, verification theater y fallbacks especulativos. [cdrcthv/deslop](https://github.com/cdrcthv/deslop) (8 estrellas, oct 2026) es más *prevención*: diffs chicos, buscar antes de escribir, comentarios cortos.
- CodeRabbit, Greptile, Graphite Agent (antes Diamond), Cursor Bugbot y Codex `/review` son sobre todo **cazadores de bugs en el PR**, no desloppers. Se complementan: la skill limpia el diff; el reviewer de otro harness/modelo busca defectos después.
- Lo que sí está maduro son los detectores deterministas (jscpd, knip/vulture/deadcode, Semgrep/ast-grep, ruff, Sonar/Radon, Stryker/mutmut). Deben correr *antes* del LLM, y el LLM no debe «redescubrir» lo que ya caza el linter.

**Recomendación para Fintoc.** Una skill propia, *diff-scoped* por defecto, con fases: (0) congelar invariantes de pagos y armar la red de seguridad, (1) scanners deterministas, (2) pasada semántica del LLM, (3) plan con severidad, (4) aplicar solo lo de bajo riesgo o lo aprobado, (5) tests + review de un segundo modelo. Por defecto no reescribe el repo entero ni toca caminos de dinero, idempotencia, tenant, máquinas de estado o contratos externos. Ante la duda, no borrar. La skill resultante es [`personal:slop-removal`](../modules/personal/skills/slop-removal/SKILL.md).

---

## 1. Taxonomía de olores en código generado por AI, con evidencia

### 1.1 Lo que miden los repos reales (no benchmarks de HumanEval)

**GitClear 2025 — *AI Copilot Code Quality*** (feb 2025). 211 millones de líneas cambiadas, 2020–2024, en repos de Google, Microsoft, Meta y empresas. Hallazgos principales, según la página del estudio y el recuento cuidadoso de Biggerstaff:

- Líneas clasificadas como *moved* (refactor/reuso) cayeron de ~25 % en 2021 a menos de 10 % en 2024.
- Líneas *copy/pasted* (clonadas) subieron de 8,3 % a 12,3 % en el mismo periodo. 2024 es el primer año en que copy/paste supera a *moved*.
- Churn a dos semanas (líneas revertidas o actualizadas en < 14 días): 3,1 % (2020), 3,3 % (2021–2022, baseline pre-AI que ellos mismos usan), 4,5 % (2023), 5,7 % real en 2024 (habían proyectado 7,1 % y lo bajaron en el apéndice). Es un *doblaje sobre una base chica*, no un 40 %.
- El título del reporte habla de «4x more code cloning»; el 2026 resume el hallazgo de 2025 como que los commits que contienen un bloque duplicado subieron ~10× en dos años. Son métricas distintas del 8,3 % → 12,3 % de líneas copy/paste. Conviene citar el número concreto, no el multiplicador del título.

Fuentes: [página 2025](https://www.gitclear.com/ai_assistant_code_quality_2025_research); tabla de churn en [Biggerstaff, ago 2026](https://www.mikebiggerstaff.me/writing/gitclear-40-percent).

**GitClear 2026 — *The Maintainability Gap*** (datos 2023–2026 YTD, 623 millones de cambios). El mensaje editorial es explícito: el titular no es «la AI escribe mal código», sino que el workflow por defecto entrega código atómico y acumula deuda en reuso y visibilidad de errores. Señales (índice 2023 = 100, o niveles absolutos cuando la página los da):

| Señal | Número | Lectura para slop |
|---|---|---|
| Duplicación de bloques (≥ 5 líneas significativas repetidas), por millón de líneas cambiadas | 40,3 (2023) → 73,0 (2026 YTD), **+81 %** | Clones que imponen un «impuesto de propagación» |
| Copy/paste intra-commit | 9,4 % (2022) → **15,7 %** (1S 2026) | Pegar en vez de extraer o reusar |
| Código *moved* (refactor) | 21 % (2022) → 13 % (2023) → **3,8 %** (2026 YTD), **−70 %** vs 2022 | Casi no se consolida |
| Llamadas a métodos de otro archivo / conectividad | 343 → 223 por mil líneas, **−35 %** | Archivos autosuficientes, helpers reinventados |
| Mantenimiento de legado (cambios a código de > 12 meses) | 1,7 % → 0,46 %, **−74 %** vs 2023 | El repo crece «hacia afuera» en v1 eternas |
| Constructs que enmascaran errores | **+47 %** | Ruido defensivo / swallow de excepciones (el PDF metodológico está detrás de un formulario; no se cita un desglose más fino) |
| Churn a dos semanas | **+15 %** | Más retrabajo temprano |

GitClear también reporta (ene 2026, *AI Coding Tools Attract Top Performers*) que los heavy users producen 4–10× más que los no usuarios, pero *la mayor parte de esa brecha ya existía antes de la AI*; el ganancia frente a sí mismos sería ~25 % de velocidad. Es un dato de contexto, no de calidad.

Cinco «tripwires» que el propio whitepaper recomienda a líderes: presupuestar refactor y legado; alarma en bloques duplicados; revisar enmascaramiento de errores de forma explícita; coaching donde el juicio es más delgado; medir estructura, no solo volumen. Fuente: [The Maintainability Gap](https://www.gitclear.com/the_ai_code_quality_maintainability_gap).

**Popescu et al., *Investigating Autonomous Agent Contributions in the Wild*** ([arXiv:2604.00917](https://arxiv.org/abs/2604.00917), abr 2026; también MSR 2026). ~110.000–111.969 PRs públicas (jun–ago 2025) de Codex, Claude Code, GitHub Copilot, Google Jules y Devin, más humanos. Hallazgos que importan, sin inventar porcentajes que solo están en figuras:

- La actividad de agentes crece, pero una fracción grande cae en repos de 0 estrellas (p. ej. ~75 % de las PRs de Codex y Jules en la muestra). Eso sesga cualquier promedio «en la industria».
- El código de agentes, una vez mergeado, tiene **menor supervivencia de líneas** y **mayor churn** que el humano a 3 días, 1 semana y 3 semanas. Las diferencias son estadísticamente significativas (`p < 0.001`), con tamaños de efecto *chicos* (Cliff’s δ ≈ −0,05 a −0,14 en supervivencia; δ ≈ 0,04–0,29 en churn/borrado). Casi la mitad de los commits humanos conservan *todas* sus líneas a los tres días; los de agentes, menos.
- El churn humano se concentra sobre todo entre 0 y 0,4 (churned LOC / total LOC del commit). Los agentes tienen mediana más alta; Claude se concentra entre 0,8 y 1, lo que los autores asocian a commits que tocan porciones más grandes (a veces formato, markdown o estilo). La mayor parte del retrabajo ocurre en los primeros días.
- Amenazas que el paper declara: atribución imperfecta (Claude permite apagar watermarks; Codex a menudo commitea con la cuenta del dev), comparabilidad difícil entre agentes, y mayoría de actividad en repos chicos.

Es la mejor fuente *en salvaje* para «el código de agentes se reescribe pronto». No es un veredicto de que el 40 % se tire.

### 1.2 Lo que miden los estudios de laboratorio (calidad estática, smells, tests flojos)

**Paul, Zhu y Bayley, *Investigating The Smells of LLM-generated Code*** ([arXiv:2510.03029](https://arxiv.org/abs/2510.03029), oct 2025; extensión de ICCBDC 2025). Java generado por Gemini Pro, ChatGPT, Codex y Falcon, comparado con soluciones de referencia profesionales. Incidencia de smells *mayor* que la baseline: Falcon +42,28 %, Gemini Pro +62,07 %, ChatGPT +65,05 %, Codex +84,97 %. Promedio +63,34 % (implementation smells +73,35 %, design smells +21,42 %). El aumento es mayor en tareas más complejas y en temas más avanzados (p. ej. OO).

**Huang et al., *Beyond Functional Correctness*** ([arXiv:2610.19167](https://arxiv.org/abs/2610.19167), oct 2026). 65.663 programas Python de 73 modelos en LiveCodeBench, evaluados con Pylint, Radon y SonarQube. La correctitud funcional no captura la calidad: hay diferencias sistemáticas de mantenibilidad entre modelos, y acertar el test a menudo viene con trade-offs estructurales (más complejidad, no soluciones más simples). Motiva exactamente el combo «scanner estático + juicio», no solo «los tests pasan».

**Liu et al., *Refining ChatGPT-Generated Code*** ([TOSEM 2024](https://dl.acm.org/doi/10.1145/3643674); [arXiv:2307.12596](https://arxiv.org/abs/2307.12596)). 4.066 programas Java/Python de LeetCode: 2.756 correctos, 1.082 con output incorrecto, 177 con error de compilación/runtime; 1.930 con problemas de estilo/mantenibilidad. La reparación iterativa con feedback de análisis estático ayuda más en estilo que un «arréglalo» genérico. Es anterior a la era agentica, pero ya documentaba que *pasar el caso* ≠ código sano.

**Siddiq et al., *Using Large Language Models to Generate JUnit Tests*** (EASE 2024, [arXiv:2305.00418](https://arxiv.org/html/2305.00418v4)). Codex, GPT-3.5-Turbo y StarCoder. Codex supera 80 % de coverage en HumanEval, pero **ningún modelo pasa de 2 % de coverage en SF110** (código de proyectos reales). Hay test smells que EvoSuite no introduce: Empty Tests, Redundant Assertion, Redundant Print, Constructor Initialization. En SF110, Empty Tests (EM): Codex 2K **7,2 %**, Codex 4K 1,3 %, StarCoder 3,8 %, GPT-3.5 0 %. El 96,7 % de los tests de StarCoder tenía al menos un smell. Implicación directa para la skill: un test generado que «pasa» puede no estar testando nada, o no estar testando el sistema real.

Un estudio de 2023 en C# (Steenhoek et al. / *Reinforcement Learning from Automatic Feedback…*, [arXiv:2310.02368](https://arxiv.org/abs/2310.02368)) reportó que el 31 % de tests de un Codex base no tenían asserts. Tratarlo como dato de una generación anterior de modelos, no como tasa actual.

### 1.3 Productividad, inestabilidad y «PRs que pasan tests pero no se pueden mergear»

**METR, julio 2025** ([blog](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/), [arXiv:2507.09089](https://arxiv.org/pdf/2507.09089v2)). RCT con 16 devs experimentados en repos OSS propios, 246 issues, Cursor Pro + Claude 3.5/3.7 Sonnet (herramientas early-2025). Con AI tardaron **19 % más**. Esperaban un 24 % de aceleración y, después de vivir la ralentización, *seguían creyendo* que la AI los había acelerado un 20 %. METR advierte que el resultado es un snapshot, no un veredicto eterno, y no se generaliza a juniors o a codebases desconocidos.

**METR, 24 feb 2026** ([actualización](https://metr.org/blog/2026-02-24-uplift-update/)). El follow-up late-2025 / early-2026 quedó sesgado: mucha gente ya no quiere trabajar sin AI, y elige no someter las tareas donde más espera ganancia. Los números crudos muestran posible speedup (−18 % de tiempo en el subconjunto de participantes originales; IC amplio), pero METR los considera evidencia *débil*. No usar este update para afirmar que «ahora la AI sí acelera X %».

**METR, 12 ago 2025, evaluación algorítmica vs holística** ([blog](https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons/)). En un subconjunto de 15 PRs de un agente (Claude 3.7 Sonnet en scaffold ReAct): *ninguna* era mergeable tal cual. Incluso cuando pasaban los tests escritos por el maintainer, estimaron ~26 minutos de arreglo (mínimo 15). De las PRs que pasaban tests (n=4): 100 % con coverage de tests inadecuado, 75 % con docs flojas, 75 % con lint/tipos, 50 % con otros problemas de calidad (verboso, frágil, difícil de mantener). Todas las 15 PRs tenían al menos tres de esas cinco clases de fallo. Esto es la definición operativa de slop + tests débiles: el oráculo del benchmark no basta.

**DORA 2025, *State of AI-assisted Software Development*** (encuesta 13 jun–21 jul 2025; anuncio [23 sep 2025](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report); [pub de Google](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/); [PDF Thoughtworks / resumen](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_report_state_of_ai_assisted_software_development_2025.pdf)). Casi 5.000 profesionales.

- 90 % usa AI en el trabajo; más del 80 % cree que le subió la productividad; **30 % tiene poca o nula confianza** en el código generado.
- El 59 % *percibe* mejora de calidad de código (7 % «extremely», 21 % «moderately», 31 % «slightly»); 30 % sin impacto; 7 % un poco peor. Es percepción, no medición de clones/churn.
- A diferencia de 2024, la adopción de AI se asocia a **más throughput**, pero **sigue asociada a más inestabilidad** de entrega. La tesis: la AI es un amplificador; sin tests automatizados, versionado maduro, batches chicos y plataformas internas, la velocidad se va a caos downstream.
- El modelo de capacidades incluye, entre otras, **trabajar en batches chicos** precisamente para contrarrestar el riesgo de que la AI genere cambios grandes e inestables, y **version control fuerte** como red de seguridad.

Implicación para la skill: un limpiador que reescribe medio repo en un solo commit es parte del problema que DORA describe, no de la solución.

### 1.4 Taxonomía operativa (para la skill)

Síntesis de las fuentes de arriba más las recetas de `/deslop` y `/simplify`. Cada ítem es un *hallazgo candidato*, no una regla de borrado automático.

1. **Duplicación y helpers reinventados.** Bloques copiados, la misma política en tres archivos, un `formatAmount` nuevo cuando ya existe uno. Señal GitClear más cara a largo plazo.
2. **Código muerto.** Imports, funciones, flags, ramas y archivos que nadie llama. Detectable en gran parte de forma determinista.
3. **Sobre-abstracción y flexibilidad especulativa.** Factories, interfaces de un solo implementor, wrappers, «por si acaso» y fallbacks que nunca se ejercitan (el ángulo de [deslop-GPT](https://github.com/MrZoyo/deslop-GPT)).
4. **Ruido defensivo.** Null checks, type guards y `try/catch` en límites *internos* ya confiables; catches vacíos o demasiado anchos (señas de error-masking). En un PSP esto es peligroso: a veces el check *es* el invariante.
5. **Comentarios y docs de relleno.** Narrar el *qué*; JSDoc/docstrings metidos en un archivo que nunca los usó; READMEs o comentarios de sección tipo tutorial.
6. **Inconsistencia de patrón.** `any`/casts para callar al typechecker, `let` vs `const` distinto al archivo, nueva convención de nombres, reformateos de drive-by.
7. **Bugs silenciosos.** Swallow de errores, happy-path incorrecto, condiciones invertidas, tests que mockean el bug. El limpiador *los reporta*, no los «arregla» de pasada mezclados con estilo.
8. **Tests que no testean.** Empty tests, asserts tautológicos (`expect(true)`), tests que solo verifican que el mock fue llamado, coverage alto con mutantes vivos, «verification theater» (muchas pruebas de andamiaje, ninguna del comportamiento de negocio).
9. **Diffs inflados / rewrites de drive-by.** +1000/−1000, archivos no pedidos, reordenar para «dejar lindo». Anti-patrón de [Willison](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/) y de [cdrcthv/deslop](https://github.com/cdrcthv/deslop).
10. **Código aislado, no tejido al sistema.** Archivos nuevos autosuficientes en vez de extender el módulo canónico (caída de conectividad de GitClear).

---

## 2. Herramientas, plugins, prompts y prácticas

### 2.1 Anthropic: `code-simplifier` y `/simplify`

El 9 de enero de 2026, Boris Cherny mergeó el plugin oficial [`code-simplifier`](https://github.com/anthropics/claude-plugins-official/pull/183) en [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official) (47.963 estrellas al 22 nov 2026). El agente ([`agents/code-simplifier.md`](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-simplifier/agents/code-simplifier.md)) está pensado para Opus y opera así:

- Solo código *recientemente modificado*, salvo instrucción contraria.
- **Preservar funcionalidad exacta**: no cambiar qué hace el código, solo cómo.
- Subir claridad: menos anidación, menos redundancia, mejores nombres, menos comentarios obvios, evitar ternarios anidados.
- Evitar la sobre-simplificación (one-liners opacos, juntar demasiadas responsabilidades, borrar abstracciones útiles).
- Algunas reglas del markdown del plugin (ES modules, `function` vs arrows, tipos explícitos, «evitar try/catch when possible») son *estándares del propio repo de Anthropic / CLAUDE.md*, no leyes universales. Una skill de Fintoc no debe copiarlas al pie de la letra.

En paralelo, Claude Code incluye la skill embebida **`/simplify [target]`** ([referencia de comandos](https://code.claude.com/docs/en/commands), actualizada en 2026): revisa el código cambiado (o un path/PR) y *aplica* las limpiezas. Lanza **cuatro agentes en paralelo**: reuso de helpers existentes, simplificación, eficiencia, y si el cambio está en el nivel correcto de abstracción. **No busca bugs de correctitud**; para eso está `/code-review` (alias `/review`), que sí puede ir con `--fix` o `ultra` (review profundo en la nube). El equipo de Claude Code, en sus [power user tips](https://support.claude.com/en/articles/14554000-claude-code-power-user-tips) (actualizados ~3 semanas antes de esta pesquisa), recomienda appendear `/simplify` después de un cambio y declara que el tip #1 es la **verificación**: el agente tiene que poder chequear su propio output (tests, comandos, browser). También documentan worktrees nativos (`claude --worktree`), alineado con Conductor.

Diseño a robar: *cleanup ≠ bug hunt*; scope al diff; varios lentes en paralelo; preservar comportamiento; verificar.

### 2.2 Codex: `/review` y reglas en `AGENTS.md`

Codex CLI puede revisar cambios locales o un PR (documentación de review en el centro de ayuda de ChatGPT / [blog de reglas custom](https://developers.openai.com/blog/custom-code-review-rules-for-codex)). Las reglas duraderas van en una sección `## Code Review Rules` de `AGENTS.md` (repo-wide en la raíz, específicas en el servicio). OpenAI reporta que, en su eval interna, las variantes guiadas por reglas recuperaron **el 98 %** de los findings custom exigidos, frente a **58,3 %** del control. El consejo de autoría es el que una skill de pagos debería copiar para *invariantes*: una regla corta, el comportamiento inseguro, y el camino seguro; nada de lint (eso es CI); no reglas tan anchas que llenen de ruido.

Skills de Codex: se descubren en **`.agents/skills/`** subiendo desde el CWD hasta la raíz del repo, más `~/.agents/skills` ([docs oficiales *Build skills*](https://learn.chatgpt.com/docs/build-skills)). Cada skill es un directorio con `SKILL.md` (`name` + `description`) y opcionalmente `scripts/`, `references/`, `assets/`. Eso confirma la convención que pediste, distinta de `.codex/skills/` que aún aparece en READMEs comunitarios viejos.

### 2.3 Reviewers comerciales (complemento, no sustituto del deslop)

Estos productos viven en el PR y optimizan *bugs accionables*. Sirven de segunda pasada, no como la skill de limpieza.

- **Cursor Bugbot** ([docs](https://cursor.com/docs/bugbot), [update 10 jun 2026](https://cursor.com/blog/bugbot-updates-june-2026)): review de diffs en GitHub/GitLab/etc. En jun 2026 anunciaron `/review` (y `/review-bugbot`) *antes de pushear*, review incremental de lo nuevo, y que el 90 % de las corridas termina en menos de 3 minutos (modelo Composer 2.5). Si corres `/review` y luego abres el mismo diff como PR, no re-revisa de cero.
- **Graphite Agent**, antes **Diamond** ([docs de AI Reviews](https://graphite.com/docs/ai-reviews)): se vende como enfocado en bugs reales (lógica, edge cases, seguridad, performance), no en estilo, con contexto de todo el repo y encaje en PRs apilados.
- **CodeRabbit** ([overview](https://docs.coderabbit.ai/guides/code-review-overview)): summaries + comentarios incrementales, linters/SAST integrados. Útil, con riesgo conocido de ruido si no se calibra.
- **Greptile**: se posiciona por contexto de grafo / bugs arquitectónicos cross-file (su propia comparativa 2026: [best AI code review tools](https://www.greptile.com/content-library/best-ai-code-review-tools)).

Ninguno reemplaza un paso *behavior-preserving* de delete-first sobre el diff. Varios benchmarks de 2026 discuten falsos positivos (p. ej. [Macroscope](https://macroscope.com/content/ai-code-review-false-positives-signal-to-noise), [crbench / Drape](https://drape.io/benchmark/)); las cifras de marketing («10 % más bugs») hay que tomarlas como claims de vendor.

### 2.4 Skills open source «deslop» / «remove-ai-slop»

Estrellas según GitHub API, 22 nov 2026. Muchos repos llamados «deslop» son para *prosa* (papers, legales, README). Se listan aparte para no mezclarlos.

**Enfocadas en código (o con un pie claro en código):**

| Repo | Estrellas | Fecha | Qué hace de verdad |
|---|---|---|---|
| [MrZoyo/deslop-GPT](https://github.com/MrZoyo/deslop-GPT) | 141 | push oct 2026 | Deletion-first: test bloat, verification theater, fallbacks especulativos, preservar comportamiento |
| [cdrcthv/deslop](https://github.com/cdrcthv/deslop) | 8 | creado 24 oct 2026 | Skill + comandos `/deslop-*` para *escribir* diffs revisables (~300 líneas, buscar antes de escribir, comentarios de *por qué*, hand-off de 10 s). Más prevención que limpieza quirúrgica |
| [bjcoombs/ai-native-toolkit](https://github.com/bjcoombs/ai-native-toolkit) | 34 | activo nov 2026 | Toolkit más amplio; incluye un `/deslop` |
| [gabelul/slopbuster](https://github.com/gabelul/slopbuster) | 48 | jul 2026 | Prosa *y* código; 152 patrones; no es un workflow de refactor con tests |
| [chrisliu298/deslop](https://github.com/chrisliu298/deslop) | 1 | 14 mar 2026 | La receta más clara de *limpiar el diff*: comments de relleno, defensivos internos, variables de un solo uso, casts redundantes, dead code, estilo del archivo como guía. «When in doubt, leave it in.» Basada en el prompt de @lucasb-eyer. Instala en `~/.claude/skills/deslop` (y documenta `~/.codex/skills/`, path ya no canónico) |
| [diegopetrucci/remove-ai-code-slop](https://github.com/diegopetrucci/remove-ai-code-slop) | 0 | abr–jun 2026 | Misma idea de diff vs base branch, review-first opcional |

El `SKILL.md` de chrisliu298 (leído en raw el 22 nov 2026) es el mejor punto de partida táctico, con un hueco importante para Fintoc: **no corre tests, no llama scanners, no tiene invariantes de dominio, y aplica ediciones en silencio**. Una skill seria tiene que añadir esas tres cosas.

**Prosa / no usar como base de la skill de código:** [stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop) (445, escritura científica), [shessenauer/deslop-ai-lint-skill](https://github.com/shessenauer/deslop-ai-lint-skill) (3, docs), [glaforge/deslopify](https://github.com/glaforge/deslopify) (43, Gemini CLI para texto), etc.

Hay también un listing genérico «deslop» en marketplaces tipo Flowy, con un SKILL.md de unas pocas viñetas (comments, try/catch, `any`, early returns). Es demasiado delgado para un PSP.

### 2.5 Prácticas de practitioners

- **Simon Willison**, *Agentic Engineering Patterns — Anti-patterns* ([guía](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/)): no infligir a un colega código de agente sin revisar; PRs chicos; revisar también la descripción del PR (los agentes escriben narraciones convincentes); dejar evidencia de prueba manual. Principio útil: «AI should help us produce *better* code», no solo más.
- **Andrej Karpathy.** El término *vibe coding* y la advertencia posterior de mantener la AI «on a tight leash» circulan en [cobertura de abr 2025](https://visualstudiomagazine.com/articles/2025/04/25/vibe-coding-pioneer-advises-tight-leash-to-rein-in-ai-bs.aspx) y en el propio hilo. Lo que se ha *empaquetado* como skill comunitaria («Karpathy Guidelines»: declarar supuestos, implementación mínima, editar solo lo pedido, verificar criterios de éxito) son derivados ([ejemplo](https://github.com/multica-ai/andrej-karpathy-skills), [writeup may 2026](https://flowhat-blog.pages.dev/blog/2026-05-06-how-to-use-karpathy-guidelines/)), no un repo oficial suyo. Útil como ethos; no citarlo como especificación de Karpathy.
- **Equipo de Claude Code** (tips citados arriba): plan → implementar → `/simplify` → verificación. Worktrees en paralelo. No fusionar simplify y code-review en un solo monstruo.
- **Michael Feathers**, *Working Effectively with Legacy Code* (2004, sigue vigente): si vas a tocar código sin tests, primero **characterization tests** que documentan el comportamiento actual. El limpiador no puede «simplificar» un camino de pagos sin esa red.

---

## 3. Detectores deterministas para emparejar con el LLM

El LLM es bueno en duplicación *semántica* (dos helpers que hacen lo mismo con otros nombres), sobre-abstracción y comentarios de *qué* vs *por qué*. Es mediocre y caro como clon-detector o como unused-export linter. La skill debe invocar, si están en el repo o se pueden correr con `npx`/`pipx` de forma barata, y **no reportar de nuevo** lo que ya quedó verde/rojo en la herramienta.

| Problema | Herramientas | Notas de uso en el flujo |
|---|---|---|
| Clones textuales / Type-1–2 | [jscpd](https://github.com/kucherenko/jscpd), PMD CPD | Correr *sobre el diff* o con umbral alto (p. ej. ≥ 5–10 líneas, como GitClear) para no ahogarse. Output = lista de pares para que el LLM decida si consolidar |
| Clones y patrones semánticos / empty catch / `any` | [Semgrep](https://semgrep.dev), [ast-grep](https://ast-grep.github.io) | Reglas locales del monorepo > reglas genéricas. Ideal para `except: pass`, catches vacíos, `as any`, asserts tautológicos |
| Código / exports muertos | [knip](https://github.com/webpro/knip) (JS/TS, el más actual), ts-prune (más viejo), [vulture](https://github.com/jendrikseipp/vulture) (Python), `deadcode` (Go) | Falsos positivos en reflection, entrypoints y plugins. Nunca borrar sin confirmar el grafo de usos |
| Estilo, complejidad local, imports | [Ruff](https://docs.astral.sh/ruff/), ESLint, RuboCop, Credo, etc. según el stack | La skill *no* reformatea el repo; si CI ya lo cubre, no lo comenta |
| Complejidad / smells clásicos | SonarQube/SonarCloud, Radon (Python), Lizard, CodeClimate | Usar como señal, no como umbral sagrado. Huang et al. 2026 justifican este lente para código de LLM |
| Tests débiles | [Stryker](https://stryker-mutator.io) (JS/TS, .NET, Scala…), [mutmut](https://mutmut.readthedocs.io) (Python), PIT (Java) | El oráculo de «este test no testea»: si el mutante vive, el test es teatro. Stryker tiene modo [incremental](https://stryker-mutator.io/docs/stryker-js/incremental/) para no pagar el repo entero. Caro: reservar a archivos de dinero o a tests *nuevos* en el diff |
| Secrets / bugs obvios | Semgrep, linters de CI, `gitleaks` | Fuera de scope de slop, pero un catch que traga un error de firma de webhook es P0, no estilo |

Orden recomendado: tool → LLM interpreta y filtra → plan. Nunca al revés (el LLM inventando clones que jscpd no ve, sin pegar el código).

---

## 4. Patrones de workflow

### 4.1 Cuándo correrlo, y sobre qué

Consenso de `/simplify`, chrisliu298/deslop, Bugbot y DORA (batches chicos):

- **Por defecto, sobre el diff de la rama o del worktree**, no sobre el repo. Orden de desempate, copiado de deslop: `git diff --cached` → `git diff` → `git diff origin/<base>...HEAD` (merge-base, no un diff de dos puntas que mezcle ajeno).
- **Momento:** al cerrar una sesión de agente, *antes* de abrir el PR (en el worktree de Conductor). Segunda vez opcional si el PR creció. Bugbot y Codex ya permiten `/review` pre-push; el deslop debe vivir en el mismo gancho mental.
- **Repo entero** solo si Adolfo lo pide, y entonces el modo es *inventario + plan*, no un rewrite autónomo. Un cleaner que «arregla» mil archivos es una fuente de churn (justamente la señal que GitClear y Popescu miden).
- **No mezclar** un feature y un deslop en el mismo commit. Commits chicos y temáticos: (a) cosmético/comentarios, (b) dead code, (c) dedup, (d) recorte de abstracción. Así el revert es barato si algo se rompe.

### 4.2 Garantías de refactor que preserva comportamiento

1. **Tests primero.** Correr el subset relevante *antes* de editar (baseline verde). Si no hay tests del comportamiento que se va a tocar: escribir *characterization tests* (Feathers) o parar y preguntar. Borrar «código muerto» en un camino de webhooks sin test es una forma clásica de introducir un bug silencioso.
2. **No cambiar comportamiento**, salvo un bug evidente y *separado* (y en ese caso, no es slop-removal: es un fix con su test).
3. **Invariantes de pagos congelados** (sección 5): el cleaner no los «simplifica».
4. **Aplicar en racimos y re-correr tests** después de cada racimo. Si fallan, revertir ese racimo, no «arreglar el test» para que se calle, salvo que el test fuera tautológico *y* eso esté explícito en el plan.
5. **Reviewer distinto.** Ideal: otro modelo u otro harness (`/code-review`, Codex `/review`, Bugbot) sobre el diff *ya limpio*. Anthropic separa `/simplify` de `/code-review` por una razón. METR mostró que pasar tests del autor no implica mergeability.
6. **El humano sigue siendo el autor del PR.** Willison: no descargar en el revisor un diff que el autor no leyó. La skill produce un informe corto (qué se borró, qué se conservó y por qué, cómo se verificó).

### 4.3 Guardas contra el propio cleaner

El limpiador es otro agente, y puede introducir slop o bugs (sobre-simplificar un retry, unir dos helpers que no eran iguales, borrar un null check que era un invariante de tenant). Guardas concretas:

- Ante la duda, dejarlo (`under-removal is safer`, chrisliu298).
- Nunca `git add -A` ni force-push. No unstage lo que el usuario ya tenía staged (deslop lo pide explícitamente).
- Límite de blast radius: p. ej. no tocar archivos fuera del diff; no crear abstracciones nuevas «para dejar más limpio»; no renombrar símbolos públicos ni contratos.
- Stop conditions: tests rojos que no se revierten al deshacer el racimo; archivo de invariantes; ambigüedad semántica (¿estos dos `to_cents` son iguales?); el diff de limpieza se vuelve más grande que el feature.
- Un segundo par de ojos automático, *otro* sistema.

### 4.4 Cómo encaja en Conductor + worktrees

Cada tarea ya vive en un worktree. La skill debe ser **de repo** (commiteada), no solo de `~/.claude`, para que todos los worktrees y todos los agentes la vean:

```
<repo>/.claude/skills/slop-removal/SKILL.md   # Claude Code
<repo>/.agents/skills/slop-removal/SKILL.md   # Codex (canónico 2026)
```

Se puede mantener un solo directorio canónico y symlink el otro, para no divergir. Invocación típica, al final de una tarea: `/slop-removal` o «limpia el slop del diff, no apliques todavía». Encadenar, al estilo Claude: `/slop-removal /code-review` después, o Codex `/review` en el mismo worktree. No hace falta un bot de CI que reescriba main.

---

## 5. Recomendación: diseño de la skill

La skill ejecutable es [`personal:slop-removal`](../modules/personal/skills/slop-removal/SKILL.md). Aquí, la justificación.

### 5.1 Qué no sea

- No es un formatter, ni un linter, ni `/code-review`.
- No es un rewrite de arquitectura.
- No aplica un estilo «Anthropic» (tipos explícitos, `function` keyword, prohibir try/catch) encima del de Fintoc. **El archivo existente es la guía de estilo**, como en chrisliu298.
- No deslop de prosa (READMEs, posts). Otro problema, otras skills.

### 5.2 Fases

| Fase | Qué hace | Stop si… |
|---|---|---|
| **0. Alcance y red de seguridad** | Determinar el diff; leer `AGENTS.md`/`CLAUDE.md`; listar archivos de dinero/idempotencia/tenant en el diff; correr tests relevantes (baseline). Si no hay tests y el diff toca invariantes → parar | Baseline roja; invariantes en el diff y el usuario no pidió un plan-only |
| **1. Scanners deterministas** | jscpd/CPD, knip/vulture/deadcode, Semgrep/ast-grep, linters ya del repo, opcional Stryker/mutmut *solo* en tests nuevos o paths de dinero | La herramienta no está: omitir, no inventar su output |
| **2. Pasada semántica (4 lentes)** | Como `/simplify`: (a) reuso de helpers, (b) simplificación/ruido defensivo/comentarios, (c) dead code y consistencia, (d) tests vacíos / teatro / mutantes. En paralelo mental o con subagentes. Leer el *archivo completo*, no solo el hunk | — |
| **3. Informe y plan** | Hallazgos con severidad, ancla `path:line`, evidencia, acción propuesta, y qué *no* se toca. Por defecto **no edita** | El usuario no aprobó `--apply` / «aplicalo» |
| **4. Aplicación (opt-in)** | Solo P3 automático si se pidió apply; P2 con plan aceptado; nunca P1 de invariantes como «limpieza». Racimos + tests | Test rojo → revertir el racimo |
| **5. Verificación y hand-off** | Tests otra vez; opcional reviewer de otro modelo; resumen de 10 s estilo cdrcthv (qué cambió, qué se reutilizó, dónde mirar, cómo se testeó) | El review de bugs encontró una regresión: revertir o fijar *aparte* |

### 5.3 Severidad

- **P1 — no «limpiar», escalar.** Posible cambio de comportamiento en dinero, idempotencia, tenant/authz, máquina de estados, retries, contratos de API/webhooks; catch que traga un error de frontera; test vacío en un camino de pagos.
- **P2 — proponer, no auto-aplicar.** Duplicación no trivial, helper reinventado, dead code con alguna duda, sobre-abstracción, tests tautológicos fuera de invariantes.
- **P3 — cosmético, auto-aplicable solo con `--apply` y tests verdes.** Comentarios que narran el *qué*, variables de un solo uso, JSDoc inconsistente con el archivo, casts redundantes, defensivos claramente internos.

Confianza baja → no se aplica; se lista como `?`.

### 5.4 Invariantes de pagos que la skill no debe tocar

Copiados y adaptados de la checklist de review que ya usamos en Fintoc (work mode). El cleaner puede *reportar* una violación si el diff la introduce, pero no «simplificarla»:

- **Dinero:** enteros en unidad menor (centavos / minor units) o `Decimal` con escala explícita; la moneda viaja con el monto; **prohibido float**; regla de redondeo explícita; **CLP tiene 0 decimales** (no asumir 2).
- **Idempotencia:** toda mutación disparada desde afuera (POST, webhook, job retreable) tiene clave; la clave cubre *todo* el side effect; el replay devuelve lo mismo; hay unique constraint en DB.
- **Tenant:** toda query/mutación va scoped a org/cuenta; nada de lookups por id global solo (IDOR).
- **Máquinas de estado:** transiciones explícitas y guardadas; estados terminales inmutables; concurrencia con lock o CAS.
- **Reconciliación / ledger:** cada movimiento tiene referencia externa; los asientos cuadran; las correcciones son asientos inversos, no update/delete.
- **I/O externo:** timeouts; retry con backoff solo en llamadas idempotentes; outbox para «escribir DB + emitir evento»; timeout ≠ failure.
- **Tiempo:** instantes en UTC; fechas de negocio en TZ de negocio.
- **Datos:** nada de PII, credenciales ni números de cuenta en logs; migraciones backward compatible.
- **Contratos:** no renombrar campos de API/webhooks/eventos en un paso de «limpieza».

### 5.5 Formato de salida (hacia Adolfo, en español)

```
Alcance: <diff vs base, N archivos, +X/−Y>
Scanners: <qué se corrió, qué se omitió>
Baseline tests: <comando, verde/rojo>

Hallazgos
- [P2] path/file.ts:128 — helper `formatClp` duplica `Money.format` en lib/money.ts
  Evidencia: …  Propuesta: borrar el nuevo y usar el canónico. Tests: …

No tocado (invariantes / duda): …
Plan de commits si se aplica: …
```

Tras aplicar: el hand-off de ~10 segundos (archivos, reuso, dónde mirar, cómo se testeó).

### 5.6 Calibración pendiente

Probarla en un worktree sobre un diff real. Iterar con dos o tres PRs: calibrar umbral de jscpd, reglas de Semgrep, y qué se auto-aplica.

---

## Fuentes

Todas las URLs se visitaron o resolvieron el 22 de noviembre de 2026, salvo que se indique otra fecha de publicación.

### Estudios y reportes
- GitClear, *AI Copilot Code Quality: 2025 Data Suggests 4x Growth in Code Clones*, feb 2025: https://www.gitclear.com/ai_assistant_code_quality_2025_research
- GitClear, *The Maintainability Gap: 2026 AI Code Quality Research*: https://www.gitclear.com/the_ai_code_quality_maintainability_gap
- Mike Biggerstaff, *GitClear never published the “40% of AI code is reverted” stat*, 10 ago 2026: https://www.mikebiggerstaff.me/writing/gitclear-40-percent
- Popescu, Gros, Botocan, Pandita, Devanbu, Izadi, *Investigating Autonomous Agent Contributions in the Wild*, arXiv:2604.00917, abr 2026: https://arxiv.org/abs/2604.00917
- METR, *Measuring the Impact of Early-2025 AI…*, 10 jul 2025: https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
- METR, *We are Changing our Developer Productivity Experiment Design*, 24 feb 2026: https://metr.org/blog/2026-02-24-uplift-update/
- METR, *Research Update: Algorithmic vs. Holistic Evaluation*, 12 ago 2025: https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons/
- DORA / Google Cloud, anuncio del reporte 2025, 23 sep 2025: https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report
- DORA 2025, ficha en Google Research: https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/
- DORA AI Capabilities Model (PDF): https://services.google.com/fh/files/misc/2025_dora_ai_capabilities_model.pdf
- Paul, Zhu, Bayley, *Investigating The Smells of LLM-generated Code*, arXiv:2510.03029, oct 2025: https://arxiv.org/abs/2510.03029
- Huang et al., *Beyond Functional Correctness…*, arXiv:2610.19167, oct 2026: https://arxiv.org/abs/2610.19167
- Liu et al., *Refining ChatGPT-Generated Code*, TOSEM 2024: https://dl.acm.org/doi/10.1145/3643674 — arXiv: https://arxiv.org/abs/2307.12596
- Siddiq et al., *Using Large Language Models to Generate JUnit Tests*, EASE 2024: https://arxiv.org/html/2305.00418v4

### Herramientas, plugins, skills, prácticas
- Anthropic, plugin `code-simplifier` (PR #183, 9 ene 2026): https://github.com/anthropics/claude-plugins-official/pull/183
- Agente: https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-simplifier/agents/code-simplifier.md
- Marketplace: https://claude.com/marketplace/plugins/code-simplifier
- Claude Code, Commands (`/simplify`, `/code-review`): https://code.claude.com/docs/en/commands
- Claude Code, power user tips: https://support.claude.com/en/articles/14554000-claude-code-power-user-tips
- OpenAI, *Custom Code Review rules for Codex*: https://developers.openai.com/blog/custom-code-review-rules-for-codex
- OpenAI, *Build skills* (path `.agents/skills`): https://learn.chatgpt.com/docs/build-skills
- Cursor, Bugbot docs: https://cursor.com/docs/bugbot
- Cursor, *Bugbot is now over 3x faster…*, 10 jun 2026: https://cursor.com/blog/bugbot-updates-june-2026
- Graphite, AI Reviews (Graphite Agent, ex Diamond): https://graphite.com/docs/ai-reviews
- CodeRabbit, overview: https://docs.coderabbit.ai/guides/code-review-overview
- chrisliu298/deslop: https://github.com/chrisliu298/deslop
- cdrcthv/deslop: https://github.com/cdrcthv/deslop
- MrZoyo/deslop-GPT: https://github.com/MrZoyo/deslop-GPT
- diegopetrucci/remove-ai-code-slop: https://github.com/diegopetrucci/remove-ai-code-slop
- Simon Willison, anti-patterns: https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/
- Visual Studio Magazine, *Vibe Coding Pioneer Advises 'Tight Leash'…*, 25 abr 2025: https://visualstudiomagazine.com/articles/2025/04/25/vibe-coding-pioneer-advises-tight-leash-to-rein-in-ai-bs.aspx
- jscpd, knip, Semgrep, ast-grep, Ruff, Stryker incremental: sitios oficiales enlazados en la sección 3

### Límites de esta pesquisa
- El PDF completo de GitClear 2026 está detrás de un formulario; se usó el abstract público de la landing (la versión en `gitkraken.gitclear.com` devolvió 503; `www.gitclear.com` sí respondió).
- Varias cifras de Popescu viven en figuras; se citan solo las que el texto afirma.
- Estrellas de GitHub: snapshot del 22 nov 2026, API pública. Las páginas HTML de GitHub a veces muestran 0 sin login; se priorizó la API.
- No se evaluó la calidad empírica de las skills comunitarias más allá de leer READMEs / SKILL.md accesibles.
