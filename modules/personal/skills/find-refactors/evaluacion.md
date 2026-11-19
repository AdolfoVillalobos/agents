# Casos de evaluación de find-refactors

Estos casos son contratos de comportamiento. No son ejecuciones con un modelo. Al correrlos, registrar la revisión de la skill, el repo y commit, el modelo y la salida. Entregar el prompt y el material sin anticipar la respuesta esperada.

| Prompt y material | Resultado esperado |
| --- | --- |
| «Busca refactors en `engines/payments` y `engines/subscriptions`». Dos servicios de detalle de medio de pago, uno por engine, cambiaron juntos en 6 commits de 90 días. | Una ficha por el acoplamiento, con el conteo, los callers de ambos y un cambio reciente que tuvo que tocar los dos. Propone un dueño único o una interfaz pública, no copiar lógica. |
| Un archivo de 600 líneas cambió 24 veces en 90 días, sin tests para la rama que se movería. | La ficha existe y el plan de PRs abre con tests de caracterización. Riesgo bajo o medio según el plan, nunca "bajo" sin cobertura. |
| El único hallazgo en un módulo es un comentario sobrante y un `let!` que debería ser `let_it_be`. | Cero fichas. Una línea de candidatos chore. No rellena el cupo. |
| Un candidato propone una clase base para un único proveedor. | Va a descartes como patrón sin segundo caso. |
| La refutación encuentra que el comportamiento fue discutido y aceptado en el PR origen. | Va a descartes como intencional, con el link al PR. |
| Un candidato toca `amount_cents` o un callback `after_commit`. | Ficha con riesgo alto, marcada no elegible. |
| «Abre los PRs». | No edita archivos ni abre PRs. Entrega las fichas para que otro paso los abra. |
