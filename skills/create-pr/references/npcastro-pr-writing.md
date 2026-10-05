# Redacción de PRs: muestra de npcastro

Consulta y lectura: **21 de septiembre de 2026**. Se leyeron los títulos y cuerpos completos de los **50 PRs más recientes por fecha de creación** de [npcastro](https://github.com/npcastro) en [fintoc-com/fintoc-rails](https://github.com/fintoc-com/fintoc-rails), incluyendo abiertos y cerrados. La muestra va del **5 de junio al 17 de septiembre de 2026**.

Esta nota documenta evidencia e inferencias; las instrucciones vigentes viven en [SKILL.md](../SKILL.md). No demuestra que una forma de escribir reduzca el tiempo de revisión: no se midieron tiempos ni resultados de revisiones.

## Método y procedencia

El nombre pedido, `fintoc/fintoc-rails`, devolvió 404 al consultar la API de GitHub. La búsqueda de repositorios devolvió `fintoc-com/fintoc-rails`; el remoto `origin` del checkout local de `fintoc-rails` apunta a `https://github.com/fintoc-com/fintoc-rails.git`. Se corrigió el nombre del repositorio, sin cambiar de autor: los 50 registros tienen `author.login = npcastro` (Nicolás Castro Leal).

Consulta reproducible:

```sh
gh pr list --repo fintoc-com/fintoc-rails --author npcastro \
  --state all --search 'sort:created-desc' --limit 50 \
  --json number,title,body,url,createdAt,updatedAt,mergedAt,state,headRefName,baseRefName,author
```

Se verificaron 50 números distintos, el mismo autor y orden descendente de `createdAt`. La consulta no filtra por estado de merge: varios títulos contienen un prefijo de Bors y el PR figura cerrado. Los cuerpos y títulos son los disponibles en la fecha de consulta, no necesariamente sus versiones iniciales.

Los datos completos y las métricas por PR quedaron en el workspace, dentro de `.context/research/`, que no se publica:

- `npcastro-fintoc-rails-last-50-2026-09-21.json`: respuesta de GitHub.
- `npcastro-pr-writing-metrics-2026-09-21.json`: conteos calculados localmente con Python.

**Definición de palabra:** token separado por espacios, después de quitar líneas de encabezados Markdown y marcadores de bullets/checklists. Se conservaron el texto de Tests, Rollback, identificadores y enlaces. Cada URL sin espacios cuenta como un token. Para títulos se retiraron el prefijo `[Merged by Bors] -` y el ID inicial `[PAY-…]`; otros prefijos permanecen. Los bullets de cambios se contaron como líneas que comienzan con `-`, con o sin checkbox; por eso un desglose detallado puede producir más de tres.

## Observaciones medidas

| Medida | Resultado |
| --- | --- |
| Extensión del título, sin los prefijos indicados | Mediana: 5 palabras; rango: 2–12 |
| Extensión del cuerpo, sin encabezados ni marcadores | Mediana: 64 palabras; rango: 7–308 |
| Cuerpos de hasta 80 / hasta 120 palabras | 32/50 / 41/50 |
| Contexto | Mediana: 16 palabras; 46/49 tienen hasta 40 |
| Bullets de cambios | Mediana: 2; 44/49 PRs tienen entre 1 y 3 |
| Extensión de cada bullet de cambios | Mediana: 9 palabras; 105/117 tienen hasta 15 |
| Plantilla Contexto → Que hay de nuevo? → Tests → Consideraciones | 49/50 |
| Consideraciones con contenido | 36/49; las otras 13 quedan vacías o con un guion |
| Encabezado Rollback | 13/50 |
| Enlaces a Linear en el cuerpo | 0/50 |

El PR [#15134](https://github.com/fintoc-com/fintoc-rails/pull/15134) solo contiene un footer de Compose: se conserva en los conteos de los 50, pero no se interpreta como ejemplo de redacción humana ni participa en las métricas de secciones. Los otros 49 cuerpos están escritos principalmente en español, con términos técnicos en inglés. Los títulos alternan español e inglés.

## Reglas inferidas para simplicidad y brevedad

Estas son recomendaciones a partir de la muestra, no reglas declaradas por el autor:

1. **Abrir con la necesidad o el fallo concreto.** Usar una o dos frases: quién necesita qué, o qué falla y bajo qué condición. En [#16938](https://github.com/fintoc-com/fintoc-rails/pull/16938), el contexto identifica el customer ausente y el cambio explica que se retorna `null`. En [#16611](https://github.com/fintoc-com/fintoc-rails/pull/16611), una restricción impide configurar la tarifa acordada. El lector entiende el motivo antes de leer implementación.
2. **Nombrar el cambio con pocas palabras y un objeto concreto.** Preferir acción + objeto en el título y entre uno y tres bullets para los efectos principales. [#16323](https://github.com/fintoc-com/fintoc-rails/pull/16323) nombra el tenant que se crea; [#16786](https://github.com/fintoc-com/fintoc-rails/pull/16786) nombra el N+1 que se corrige. Evitar convertir el cuerpo en inventario de archivos. El rango de bullets observado respalda esta preferencia; no convierte tres en un límite universal.
3. **Reservar las consideraciones para decisiones y límites que cambian la revisión.** [#16203](https://github.com/fintoc-com/fintoc-rails/pull/16203) aclara que el invoice anticipado no se persiste ni tiene ciertos campos. [#15107](https://github.com/fintoc-com/fintoc-rails/pull/15107) explica cuáles intentos cuentan y por qué. Conservar este tipo de información aunque obligue a recortar otra parte del texto.
4. **Ubicar cada PR dentro de la secuencia cuando ayude a entender su alcance.** [#16502](https://github.com/fintoc-com/fintoc-rails/pull/16502) explica que prepara el servicio y que otro PR completará los flujos. [#14814](https://github.com/fintoc-com/fintoc-rails/pull/14814) distingue la conversión ya implementada de la habilitación que viene después. Resumir esa dependencia en una frase, sin relatar todos los intentos de implementación.
5. **Convertir dudas reales en un foco de revisión concreto.** [#16737](https://github.com/fintoc-com/fintoc-rails/pull/16737) distingue mejoras propuestas de mejoras de rendimiento comprobadas. Los cuerpos extensos de [#15243](https://github.com/fintoc-com/fintoc-rails/pull/15243) y [#14576](https://github.com/fintoc-com/fintoc-rails/pull/14576) muestran cómo las alternativas y dudas acumulan texto. La recomendación es conservar la incertidumbre relevante en una frase específica, sin presentar como certeza lo que no se validó.

## Preferencias del usuario y patrones que no se trasladan

| Decisión de la skill | Relación con la muestra |
| --- | --- |
| Español por defecto para título y descripción | Es una preferencia explícita; la muestra mezcla idiomas en los títulos. |
| Objetivo de 80 palabras y máximo de 120 | Compatible con gran parte de la muestra, pero no es una regla del autor: 9/50 cuerpos superan 120 incluso sin contar encabezados. |
| Sin enlaces a Linear en la descripción | Coincide con 0/50 enlaces observados. Esto no demuestra cómo se vincularon los issues. |
| Omitir Tests cuando solo repite CI | Es una preferencia explícita: la muestra sí repite tests unitarios/de integración. No se inspeccionó la CI de cada PR ni se deduce de esas etiquetas qué tests se ejecutaron. |
| Omitir secciones vacías y frases automáticas sin información | Es una mejora propuesta sobre la muestra: aparecen Consideraciones vacías y fórmulas genéricas de rollback. |

Los nombres de ramas están en el JSON, pero **no se compararon con los nombres sugeridos por Linear**. No se infiere de esta muestra una política de branches, creación de issues ni vinculación automática. Tampoco se adopta el prefijo de Bors como parte del título a escribir.

## Ejemplo adaptado

Ejemplo editorial inspirado en [#16938](https://github.com/fintoc-com/fintoc-rails/pull/16938), no transcripción literal ni validación del código:

```markdown
[PAY-9695] Evitar errores al consultar invoices sin customer

## Contexto
Consultar una invoice desde el dashboard falla si su customer ya no existe.

## Qué hay de nuevo
- Retornar `null` en customer cuando no se encuentra.
```

Conserva el disparador y el resultado; omite Tests genéricos y Consideraciones vacías. El español, los encabezados corregidos y la omisión de Tests reflejan decisiones editoriales de la skill.

## Cobertura completa

Se leyeron título y cuerpo de todos los PRs siguientes, ordenados por creación descendente. Cada enlace es una fuente primaria de la muestra.

| PR | Creado (UTC) |
| --- | --- |
| [#17347](https://github.com/fintoc-com/fintoc-rails/pull/17347) | 2026-09-17 |
| [#17137](https://github.com/fintoc-com/fintoc-rails/pull/17137) | 2026-09-11 |
| [#16985](https://github.com/fintoc-com/fintoc-rails/pull/16985) | 2026-09-08 |
| [#16938](https://github.com/fintoc-com/fintoc-rails/pull/16938) | 2026-09-07 |
| [#16871](https://github.com/fintoc-com/fintoc-rails/pull/16871) | 2026-09-04 |
| [#16859](https://github.com/fintoc-com/fintoc-rails/pull/16859) | 2026-09-03 |
| [#16820](https://github.com/fintoc-com/fintoc-rails/pull/16820) | 2026-09-02 |
| [#16786](https://github.com/fintoc-com/fintoc-rails/pull/16786) | 2026-09-02 |
| [#16737](https://github.com/fintoc-com/fintoc-rails/pull/16737) | 2026-09-01 |
| [#16720](https://github.com/fintoc-com/fintoc-rails/pull/16720) | 2026-08-31 |
| [#16684](https://github.com/fintoc-com/fintoc-rails/pull/16684) | 2026-08-28 |
| [#16611](https://github.com/fintoc-com/fintoc-rails/pull/16611) | 2026-08-27 |
| [#16503](https://github.com/fintoc-com/fintoc-rails/pull/16503) | 2026-08-25 |
| [#16502](https://github.com/fintoc-com/fintoc-rails/pull/16502) | 2026-08-25 |
| [#16323](https://github.com/fintoc-com/fintoc-rails/pull/16323) | 2026-08-20 |
| [#16203](https://github.com/fintoc-com/fintoc-rails/pull/16203) | 2026-08-18 |
| [#16197](https://github.com/fintoc-com/fintoc-rails/pull/16197) | 2026-08-18 |
| [#16026](https://github.com/fintoc-com/fintoc-rails/pull/16026) | 2026-08-11 |
| [#16008](https://github.com/fintoc-com/fintoc-rails/pull/16008) | 2026-08-11 |
| [#15946](https://github.com/fintoc-com/fintoc-rails/pull/15946) | 2026-08-07 |
| [#15902](https://github.com/fintoc-com/fintoc-rails/pull/15902) | 2026-08-06 |
| [#15782](https://github.com/fintoc-com/fintoc-rails/pull/15782) | 2026-08-03 |
| [#15731](https://github.com/fintoc-com/fintoc-rails/pull/15731) | 2026-07-31 |
| [#15625](https://github.com/fintoc-com/fintoc-rails/pull/15625) | 2026-07-28 |
| [#15611](https://github.com/fintoc-com/fintoc-rails/pull/15611) | 2026-07-28 |
| [#15567](https://github.com/fintoc-com/fintoc-rails/pull/15567) | 2026-07-27 |
| [#15461](https://github.com/fintoc-com/fintoc-rails/pull/15461) | 2026-07-22 |
| [#15243](https://github.com/fintoc-com/fintoc-rails/pull/15243) | 2026-07-09 |
| [#15221](https://github.com/fintoc-com/fintoc-rails/pull/15221) | 2026-07-09 |
| [#15134](https://github.com/fintoc-com/fintoc-rails/pull/15134) | 2026-07-07 |
| [#15131](https://github.com/fintoc-com/fintoc-rails/pull/15131) | 2026-07-07 |
| [#15109](https://github.com/fintoc-com/fintoc-rails/pull/15109) | 2026-07-06 |
| [#15107](https://github.com/fintoc-com/fintoc-rails/pull/15107) | 2026-07-06 |
| [#15103](https://github.com/fintoc-com/fintoc-rails/pull/15103) | 2026-07-06 |
| [#14980](https://github.com/fintoc-com/fintoc-rails/pull/14980) | 2026-06-28 |
| [#14962](https://github.com/fintoc-com/fintoc-rails/pull/14962) | 2026-06-26 |
| [#14859](https://github.com/fintoc-com/fintoc-rails/pull/14859) | 2026-06-23 |
| [#14843](https://github.com/fintoc-com/fintoc-rails/pull/14843) | 2026-06-23 |
| [#14815](https://github.com/fintoc-com/fintoc-rails/pull/14815) | 2026-06-22 |
| [#14814](https://github.com/fintoc-com/fintoc-rails/pull/14814) | 2026-06-22 |
| [#14798](https://github.com/fintoc-com/fintoc-rails/pull/14798) | 2026-06-22 |
| [#14747](https://github.com/fintoc-com/fintoc-rails/pull/14747) | 2026-06-18 |
| [#14699](https://github.com/fintoc-com/fintoc-rails/pull/14699) | 2026-06-17 |
| [#14663](https://github.com/fintoc-com/fintoc-rails/pull/14663) | 2026-06-16 |
| [#14642](https://github.com/fintoc-com/fintoc-rails/pull/14642) | 2026-06-15 |
| [#14587](https://github.com/fintoc-com/fintoc-rails/pull/14587) | 2026-06-11 |
| [#14576](https://github.com/fintoc-com/fintoc-rails/pull/14576) | 2026-06-11 |
| [#14572](https://github.com/fintoc-com/fintoc-rails/pull/14572) | 2026-06-11 |
| [#14479](https://github.com/fintoc-com/fintoc-rails/pull/14479) | 2026-06-08 |
| [#14427](https://github.com/fintoc-com/fintoc-rails/pull/14427) | 2026-06-05 |
