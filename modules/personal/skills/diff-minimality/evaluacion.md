# Casos de evaluación de diff-minimality

Casos añadidos el 2026-09-22 para la revisión de tests y convenciones del repositorio. Son prompts y resultados esperados; no representan ejecuciones con un modelo.

| Prompt y contexto | Resultado esperado |
| --- | --- |
| «Simplifica el diff», con dos tests del mismo fallo bajo las mismas condiciones | Consolida la cobertura redundante e identifica el test conservado que detecta el fallo. Ejecuta los checks relevantes. |
| «Estos tests se parecen, simplifícalos», con setup común pero distintos límites o rutas de integración | Conserva los comportamientos distintos; compartir código o setup no basta para eliminar un test. |
| «Reduce tests innecesarios», con aserciones sobre métodos privados sin contrato y garantías del framework | Busca el comportamiento observable protegido. Elimina o reemplaza las aserciones redundantes sin perder cobertura necesaria; no suprime una regresión o una configuración propia de la aplicación por atribuirla al framework. |
| «Añade cobertura para este cambio», con factories, helpers y estructura de tests existentes | Inspecciona archivos comparables y sigue ubicación, nombres, fixtures, mocks y nivel de prueba del repositorio. No introduce otro patrón sin una necesidad concreta. |
| «Simplifica estos tests», donde reutilizar un helper ocultaría diferencias de dominio | Conserva el setup explícito o usa una alternativa local clara; no fuerza una abstracción por reducir líneas. |

## Validación

La revisión estructural comprueba frontmatter y formato del diff. La validación de comportamiento requiere ejecutar los casos con un agente y contrastar los cambios con la cobertura que queda; no se ha realizado todavía.
