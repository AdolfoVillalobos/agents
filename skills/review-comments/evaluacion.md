# Casos de evaluación de review-comments

Estos casos son contratos de comportamiento. No son ejecuciones con un modelo. Al correrlos, registrar la revisión de la skill, el alcance, el modelo, los comandos y la salida. Entregar el prompt y el material sin anticipar la respuesta esperada.

| Prompt y material | Resultado esperado |
| --- | --- |
| «Déjame los comentarios para pegar». El informe ya trae un defecto bloqueante: un webhook de reembolso inserta dos movimientos ante el mismo id, en una línea nueva del diff, sin constraint. | Un borrador `issue (blocking)` anclado a esa línea del lado nuevo, con escenario y evidencia en la nota privada. No publica. |
| El mismo webhook, pero el informe descartó el hallazgo porque una restricción fuera del diff ya deduplica. | No revive el comentario. El resumen no lo lista como bloqueante. |
| «Pega un nit de formato». El formateador del repositorio ya cubre ese cambio. | Omite el comentario. |
| «Comenta el diseño». El informe tiene una alternativa válida y ningún invariante roto. | `suggestion (non-blocking)` o `question (non-blocking)`, en prosa, sin fence `suggestion` que reescriba el diseño, y veredicto de aprobar con comentarios. |
| Tres renombres del mismo estilo, todos nits sostenidos por una regla escrita. | Un solo `nitpick (non-blocking)` con las otras ubicaciones. |
| Informe sin hallazgos. | Veredicto sin bloqueantes, sin comentarios y sin elogio inventado. |
| Un arreglo de una línea que el autor podría aceptar igual. | El borrador incluye un fence `suggestion` que reemplaza exactamente esas líneas, con el motivo arriba. |
| El problema está fuera del diff. | Ancla la línea cambiada más cercana y dice dónde está el problema. |
| Título y cuerpo del PR en inglés. Quien pide el review escribe en español. | El bloque para pegar sale en inglés y la nota privada en español. |
| «Publícalo» en un PR de GitHub, después de mostrar los borradores. | Envía un solo review con los comentarios en línea, sobre el SHA de head, y registra ese SHA. Un comando que solo publica el resumen no cuenta como entrega de los comentarios. |
