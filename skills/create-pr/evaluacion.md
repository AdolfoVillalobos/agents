# Casos de evaluación de create-pr

Reescritura del 2026-09-14 basada en la versión aportada por el usuario. Estos casos describen el comportamiento esperado; no son ejecuciones con un modelo.

| Prompt y contexto | Resultado esperado |
| --- | --- |
| «Abre un PR», en una rama `onb-453-feature`, con cambios y template disponibles | Lee el issue, recupera su rama sugerida y revisa el diff y los commits contra `main`; propone título en inglés con `[ONB-453]`, cuerpo en español de hasta 120 palabras y opciones Ok / Shorter / Missing something. Espera la selección antes de crear. |
| «Subamos el PR contra release», sin ID en la rama | Usa `release` como base y pide ID manual o buscar/crear un issue mediante la integración disponible. |
| «Shorter», tras mostrar una propuesta | Recorta el cuerpo, conserva las secciones aplicables y vuelve a presentar el texto sin crear el PR. |
| «Missing something: requiere coordinación con frontend» | Agrega esa coordinación en Consideraciones, respeta el límite y vuelve a presentar el texto para aprobación. |
| «Ok», tras aprobar una propuesta en GitHub | Crea un draft autoasignado al usuario autenticado con el texto aprobado. El cuerpo no contiene créditos al proveedor, modelo o agente. Verifica título, descripción, base, head y vinculación al issue, o informa qué no pudo verificar. |

## Issue y rama sugerida

| Prompt y contexto | Resultado esperado |
| --- | --- |
| «Abre un PR para ONB-453», con rama sugerida disponible y libre | Lee el issue y usa exactamente la rama sugerida, sin traducirla ni reconstruirla desde el título. Conserva el ID en el título. |
| «Crea otro PR para ONB-453», con la rama sugerida ocupada por otro PR | Crea una rama con sufijo de alcance, mantiene ONB-453 y verifica su asociación al mismo issue. No crea un issue duplicado. |
| «Actualiza este PR», con head existente distinto del sugerido | Conserva el head; usa el ID en el título y verifica la vinculación. |
| «Abre el PR», con nombre de rama fijado por el workspace y cambios locales | Conserva nombre y cambios; explica la excepción al nombre sugerido. |
| «Abre un PR para ONB-453», con integración no disponible | No inventa un nombre sugerido ni afirma haber vinculado el PR. Usa el nombre suministrado o la rama actual y el ID en el título; informa lo no verificado. |

## Enlaces e idioma

| Prompt y contexto | Resultado esperado |
| --- | --- |
| «Abre un PR», con template que contiene una URL de Linear, un ID enlazado y una definición Markdown oculta | Retira esas referencias de la descripción antes de publicar. Conserva la asociación mediante rama/título y la verifica por separado. |
| «Crea el PR en inglés» | Respeta la petición explícita para título, cuerpo y encabezados. La rama sugerida y los identificadores no se traducen. |

## Regresión: referencias de Linear dentro del contexto

| Prompt y contexto | Resultado esperado |
| --- | --- |
| «Redacta el PR» con contexto `Los pagos no se reintentan ([PAY-9838](https://linear.app/fintoc/issue/PAY-9838)).` | La descripción dice `Los pagos no se reintentan.` sin enlace, ID ni paréntesis vacíos. `[PAY-9838]` se conserva en el título. |
| Contexto copiado que termina en `(PAY-9838)` o una URL de Linear sin Markdown | Elimina la referencia completa de la descripción, en lugar de dejar el ID como texto plano. |
| Template con referencias al issue en Contexto, Consideraciones o definiciones Markdown ocultas | Revisa el cuerpo completo antes de mostrarlo y publicarlo. Ninguna sección conserva referencias al issue. La asociación se gestiona por rama/título o integración. |

## Idioma del PR

| Prompt y contexto | Resultado esperado |
| --- | --- |
| «Create a PR», con rama `onb-453-add-setup-link`, commits y template en inglés | Redacta título en inglés y descripción y encabezados en español, sin footer de atribución. Conserva `[ONB-453]`, `OrganizationSetupLink` y otros identificadores sin traducir. Ejemplo de título: `[ONB-453] Add OrganizationSetupLink model and migration`. |

## Voz y puntuación

| Prompt y contexto | Resultado esperado |
| --- | --- |
| «Redacta el PR», con una validación agregada y una comprobación ejecutada | Usa «Agregué la validación» y «Verifiqué…» cuando resulte natural. Puede describir el problema de forma impersonal. |
| «Redacta el PR», sin pruebas manuales documentadas | No escribe «Probé manualmente» ni atribuye experiencias al autor para forzar la primera persona. |
| Borrador con `Agregué validación; ahora se rechaza el monto` o `Corrige retries -- evita duplicados` | Reescribe con puntos o comas, sin punto y coma, doble guion ni raya como separadores de prosa. El título final queda en inglés. |
| El cuerpo necesita citar `bin/check --dry-run` y usar checkboxes Markdown | Conserva el comando y los marcadores. La regla de puntuación no altera sintaxis técnica. |
| «Pon solo el título en español» | Cambia el título según la petición explícita y mantiene el cuerpo en español. |
| «Pon solo la descripción en inglés» | Cambia el cuerpo y sus encabezados a inglés, conservando el título en inglés por defecto. |

## Validación en la descripción

| Prompt y contexto | Resultado esperado |
| --- | --- |
| «Abre un PR», con conteo de tests, Sorbet, rubyfmt y lint visibles en CI, sin contexto adicional de comportamiento | Omite la sección Pruebas y no repite conteos ni checks de CI. Sigue ejecutando las verificaciones requeridas por el cambio. |
| «Agrega que probé manualmente subir dos documentos y siguen visibles al recargar» | Incluye esa comprobación y su resultado en una o dos líneas de Pruebas, sin enumerar los checks de CI. |
| «Redacta el PR», sin evidencia de verificaciones ejecutadas | No inventa resultados ni copia como hecho el ejemplo de la referencia. Omite Pruebas si no aporta información; señala una brecha de validación si afecta la confianza en el cambio. |
| «Resume la validación», con 25 tests ejecutados que verifican que reintentar un pago no duplica el cobro | Describe la garantía de un único cobro en una línea. Omite el conteo, nombres de tests y resultados de Sorbet o rubyfmt, aunque la verificación haya corrido en CI. |
| «Agrega todos los tests al PR», con una lista de archivos y casos | Sintetiza el flujo o riesgo importante que quedó validado y su resultado, sin convertir Pruebas en inventario del diff. |

## Créditos y firmas automáticas

| Prompt y contexto | Resultado esperado |
| --- | --- |
| «Abre el PR», con template que termina en un footer de agradecimiento al proveedor o de generación por un agente | Elimina el footer antes de mostrar y publicar el cuerpo. No lo reemplaza por otra firma de IA. |
| «Prepara los commits», con mensaje propuesto que incluye una firma de generación y un trailer de coautoría del modelo | Omite ambos al crear el commit; conserva la explicación del cambio. |
| «Prepara los commits», con un trailer de coautoría de una persona que sí contribuyó | Conserva el crédito humano; la prohibición se limita a créditos al proveedor, modelo o agente. |

## Narrativa de commits

| Prompt y contexto | Resultado esperado |
| --- | --- |
| «Prepara los commits para el PR», con soporte multi-documento en modelo, API y formulario | Propone títulos ordenados por dependencias y agrupa cada propósito con sus tests. No separa mecánicamente implementación y tests. |
| «Prepara este cambio pequeño», con una corrección y su test | Usa un solo commit coherente si dividirlo no mejora la lectura. El mensaje identifica el resultado concreto. |
| «Ordena estos commits», con cambios locales `add support`, `fix`, `fix again` que corrigen errores de la misma rama | Integra las correcciones en el cambio correspondiente, conserva el diff final y verifica los pasos resultantes con checks relevantes. |
| «Prepara el PR», con una secuencia existente coherente y commits ajenos fuera del alcance | Conserva la secuencia y los cambios ajenos; no reescribe por una preferencia cosmética ni modifica historia compartida sin autorización aplicable. |
| «Revisa la narrativa», con un primer commit que depende de código o tests añadidos después | Reordena o agrupa para que cada paso sea coherente y verificable. Distingue los checks ejecutados de los que no pudo ejecutar. |

## Simplicidad y brevedad

| Prompt y contexto | Resultado esperado |
| --- | --- |
| «Redacta este fix pequeño», con un solo cambio observable | Una frase de contexto y un solo bullet concreto. No agrega relleno para llegar a 80 palabras ni inventa un segundo cambio. |
| «Abre el PR», con descripción inicial que recorre cada archivo | Agrupa por cambios o efectos, usa normalmente 1–3 bullets de hasta 15 palabras y elimina el recorrido de archivos. |
| «Usa los PRs de npcastro como referencia» | Adopta su contexto breve y cambios concretos. No copia prefijos del bot, tests genéricos ni cuerpos vacíos. Mantiene el título en inglés y el cuerpo en español por defecto. |
| «Describe esta limitación de compatibilidad», con un tradeoff importante | Conserva la limitación en Consideraciones y recorta detalles del diff para mantener como máximo 120 palabras. |

## Comprobación estructural

Revisar frontmatter `name`/`description`, referencias relativas existentes y presencia de las reglas de extensión y aprobación. Esto no demuestra cumplimiento del formato en una ejecución real ni valida el comportamiento entre proveedores.

Comprobación realizada el 2026-09-21: referencias relativas y anchors válidos, ejemplos breves sin enlaces de Linear y bullets de hasta 15 palabras, issue/rama antes de commits, 50 PRs únicos del autor correcto ordenados por creación y presentes en la nota de investigación. `git diff --check` pasa. No se ejecutaron los escenarios con un modelo.
