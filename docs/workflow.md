# Iterar en Conductor

## Preparar el repositorio

Conductor puede abrir un repositorio local mediante **Open project**, y crea workspaces con ramas y worktrees de Git. Los cambios que quieras llevar a un workspace deben estar en un commit. Fuente: [primer workspace en Conductor](https://www.conductor.build/docs/first-workspace).

El historial conserva un commit inicial de las 31 skills originales y un cambio posterior con esta organización y los tres drafts principales. Puedes comparar las adaptaciones con esa base o crear un worktree para iterarlas. No hace falta publicar el repositorio para trabajar localmente.

## Ciclo de una skill

1. Abre `~/.agents` con **Open project**. Si el selector oculta la carpeta, usa `Cmd+Shift+G` e introduce la ruta.
2. Crea un workspace para una mejora concreta, por ejemplo: «el review confunde sugerencias con bugs».
3. Adjunta `skills/<nombre>/SKILL.md` del workspace y un ejemplo real. Pide una modificación con un criterio observable: menos falsos positivos, hallazgos reproducibles o una descripción que explique el cambio sin contexto del chat.
4. Ejecuta el mismo caso antes y después en sesiones separadas, indicando la ruta exacta de cada versión. Guarda prompt, revisión de Git, agente/modelo, salida y juicio humano. Los resultados temporales pueden vivir en `.scratch/`; conserva los casos reutilizables junto a la skill.
5. Revisa el diff e incorpora la versión elegida a la rama principal. Esa incorporación actualiza la copia que usa la instalación personal de Codex.

No hace falta un script de setup para editar Markdown. Agrega configuración de Conductor cuando exista un comando de evaluación o una dependencia que lo justifique.

## Primeras pruebas propuestas

| Skill | Caso | Qué observar |
| --- | --- | --- |
| `code-review` | Retry que duplica un efecto; una protección existente fuera del diff; PR sin spec | Encuentra el bug real, descarta el falso positivo al leer la protección y explicita la incertidumbre |
| `diff-minimality` | Wrapper redundante junto a un guard de idempotencia necesario | Elimina complejidad sin borrar garantías ni tests útiles |
| `create-pr` | PR apilado con un cambio pequeño y una prueba que no pudo correr | Usa la base correcta, explica el cambio y declara la limitación |

Estos son casos propuestos, todavía no evaluaciones ejecutadas. La primera iteración debe usar un PR o fixture concreto y comparar las salidas; cumplir el formato de `SKILL.md` no prueba la calidad del comportamiento.
