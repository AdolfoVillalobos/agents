# Casos de evaluación de reduce-pr-risk

Estos casos son contratos de comportamiento. No son ejecuciones con un modelo. Al correrlos, registrar la revisión de la skill, la PR, el modelo y la salida. Entregar el prompt y el material sin anticipar la respuesta esperada.

| Prompt y material | Resultado esperado |
| --- | --- |
| «¿Cómo bajo el riesgo de esta PR?». La PR agrega un endpoint de reembolsos, refactoriza un serializer compartido y corrige un typo en logs. | Nivel alto por blast radius. Propone sacar el refactor y el typo a PRs previas, y dejar el reembolso chico y detrás de un flag apagado. Dice que el reembolso sigue siendo alto. |
| La PR mueve dinero de forma irreversible y ya es pequeña y está testeada. | No propone dividir más. Propone hacerlo reversible (modo prueba, cola revisada) o acepta el riesgo y pide review humano. |
| La PR solo cambia UI interna, con descripción «Implementa PAY-123». | Riesgo bajo o medio por esfuerzo de revisión. La alternativa es explicar el mecanismo en la descripción, no dividir. |
| Un refactor de lógica de conciliación sin tests que fijen el comportamiento previo. | Propone una PR anterior con tests que fijan el comportamiento actual, y después el refactor. |
| La PR actualiza snapshots para que coincidan con la nueva salida. | Lo marca como evidencia que no verifica nada y propone un test que falle si el caso cambiado está mal. |
| No hay issue enlazado. | Sigue con PR y diff, y lo reporta en «Gaps» sin tratarlo como riesgo. |
| «Divídela». | Entrega la lista de PRs en orden de merge, pero no edita, no hace push ni actualiza la PR. |
| La única alternativa es completar la descripción de la PR. | Incluye `git commit --amend --no-edit` y `git push --force-with-lease` para pedir un nuevo review de riesgo, sin ejecutarlos. |
| Una PR cambia el cálculo de comisiones (`blast_radius` `high`), con tests que ejercitan el caso y un único módulo, pero agrega una tabla nueva sin `down` (`reversibility` `high`). | Nivel `high` por piso (`blast_radius` y `reversibility` en `high`). Propone hacer la migración reversible antes que agregar tests, porque más tests no mueven el resultado. |
| Un panel admin interno (`blast_radius` `low`) toca muchos módulos relacionados (`change_scope` `mid`). | Nivel `low`: con impacto `low`, la probabilidad `mid` no sube el nivel. No propone dividir. |
