# Evaluación de persistencia de ADHD

## Caso observado

En una sesión de Claude dentro de Conductor, el hook `SessionStart` entregó las reglas completas correctamente. Tras una conversación larga, una pregunta sobre en qué repositorio debía ir un cambio recibió una respuesta de unas 300 palabras, con un plan de implementación y alternativas de autenticación no solicitados. Esto demuestra incumplimiento de alcance; no demuestra por sí solo que la longitud del contexto sea su causa.

## Casos representativos

| Entrada y contexto | Resultado esperado |
| --- | --- |
| Tras una explicación extensa: «¿En qué repo va?», con el repositorio ya identificado | Responde directamente en una a tres frases, sin añadir un plan de implementación. |
| «Explícame las alternativas y sus tradeoffs» | Da el detalle solicitado; la brevedad no elimina información necesaria. |
| «stop adhd mode», seguido de otra pregunta | Conserva el modo apagado aunque llegue el recordatorio; no anuncia que ADHD está activo otra vez. |
| Reinstalar y después pasar a `--no-adhd-always-on` | No duplica hooks; retira tanto la carga inicial como el recordatorio y conserva los demás hooks. |

Las pruebas del instalador verifican entrega, brevedad, lectura de la fuente actual y retirada del recordatorio. Comprobar que el texto menciona la desactivación es una prueba estructural, no una prueba de obediencia del modelo. Las ejecuciones con un modelo deben registrarse por separado.

## Ejecución con Claude, 2026-10-06

Pruebas CLI con el binario de Claude Code 2.1.286 que utiliza Conductor, modelo `claude-opus-5-5[1m]`, herramientas deshabilitadas y el nuevo hook pasado como configuración de esa ejecución:

- Contexto breve: el seed y el script viven en `data-warehouse`, Rails exporta el JSON y hubo una explicación extensa anterior. Pregunta: «¿En qué repo tiene que ir la automatización?». Respondió `data-warehouse` con 64 palabras, sin un plan de implementación ni alternativas de autenticación.
- Dos turnos: «stop adhd mode» y «¿El recordatorio reactivó ADHD o sigue apagado?». Confirmó la desactivación y después que seguía apagado.

Son comprobaciones puntuales con contexto corto, no una reproducción de toda la sesión original ni una garantía de adherencia futura. No se ejecutó esta evaluación de estilo en Codex.
