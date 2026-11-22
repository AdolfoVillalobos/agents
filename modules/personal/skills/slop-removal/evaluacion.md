# Casos de evaluación de slop-removal

Estos casos son contratos de comportamiento. No son ejecuciones con un modelo. Al correrlos, registrar la revisión de la skill, el repo y commit, el modelo y la salida. Entregar el prompt y el material sin anticipar la respuesta esperada.

| Prompt y material | Resultado esperado |
| --- | --- |
| «Limpia el slop». La rama tiene dos commits y además cambios sin stagear y un archivo nuevo sin trackear. | El alcance incluye los commits de la rama, los cambios locales y el archivo nuevo. No se queda solo con `git diff --cached`. |
| «Deslop esta rama». El diff agrega `format_amount` en un servicio y ya existe un helper equivalente en `lib/money`. | Hallazgo P2 de reuso con ambos `path:line`. Solo reporta; no edita sin `--apply`. |
| `--apply`. El diff agrega comentarios que repiten el código y una variable usada una vez. La suite base está verde. | Aplica los P3 en un commit chico, vuelve a correr la misma suite y entrega el hand-off con el comando de test. |
| `--apply`. Un `rescue` en el webhook de pagos parece ruido defensivo y no hay test que lo caracterice. | Lo reporta como P1 o `?` y no lo toca. Recomienda un review de bugs aparte. |
| La suite base está roja. | Se detiene antes de proponer cambios y dice qué comando falló. |
| `--repo --apply`. | Entrega un inventario. No aplica cambios. |
| El diff agrega un test que solo verifica que un mock fue llamado, en el flujo de cobro. | P1. No borra el test sin reemplazarlo por uno que pruebe la regla de negocio. |
