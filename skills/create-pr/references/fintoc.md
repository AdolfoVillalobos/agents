# Referencia de Fintoc

Esta reescritura parte de la versión de `create-pr` aportada por el usuario el 2026-09-14. Los ejemplos conservan su registro de escritura e incorporan los ajustes posteriores acordados.

## Convenciones

- Ejemplo de título: `[ONB-453] Add OrganizationSetupLink model and migration`.
- En GitHub se puede usar `gh` para crear el draft y asignarlo al usuario autenticado.

## Linear y ramas

El tracker de Fintoc es Linear. Recuperar el nombre de rama sugerido mediante la integración disponible o la acción Copy git branch name del issue. Se usa el valor devuelto tal cual, aunque esté en inglés. Una rama `onb-453-feature` corresponde a `ONB-453`.

Ejemplo ilustrativo: si Linear devuelve `adolfo/onb-453-multi-documento` y esa rama pertenece a otro PR, una variante para un alcance distinto sería `adolfo/onb-453-multi-documento-serializer`. Ambos PRs conservan `[ONB-453]` en el título. La variante es una convención de esta skill, no un nombre generado por Linear.

Linear admite asociar PRs mediante el ID en la rama o el título y varios PRs a un mismo issue. Esto permite mantener la descripción sin URLs de Linear. La asociación depende de la integración configurada y debe verificarse. Fuente: [documentación de GitHub en Linear](https://linear.app/docs/github#linking-linear-issues-to-github-prs), consultada el 2026-09-21.

## Ejemplo de narrativa de commits

Para habilitar varios documentos por slot:

1. **Permitir varios documentos en slots configurados como multi.** Incluye el flag, las restricciones y los tests del nuevo comportamiento.
2. **Exponer documents[] conservando document para clientes existentes.** Incluye la serialización y los tests de compatibilidad.
3. **Habilitar la carga múltiple en el formulario.** Incluye la interfaz y los tests del flujo.

La secuencia explica qué permite el modelo, cómo se expone y cómo se usa. Los títulos son ilustrativos; el idioma sigue las convenciones del repositorio. Cada paso contiene lo necesario para funcionar y verificarse sin depender de un commit posterior.

## Ejemplos de redacción

Para un fix pequeño basta una frase de contexto y un cambio. Ejemplo adaptado del [PR #16938 de npcastro](https://github.com/fintoc-com/fintoc-rails/pull/16938), sin repetir las validaciones visibles en CI:

```markdown
## Contexto

Consultar una invoice fallaba si no se encontraba su customer.

## ¿Qué hay de nuevo?

- [x] Devuelvo `null` como customer cuando no existe.
```

No agregar más bullets para alcanzar una cantidad. La [investigación de 50 PRs](npcastro-pr-writing.md) documenta la muestra y las diferencias entre hábitos observados y preferencias del usuario.

**Este es el registro buscado** — tres ítems de una línea, sin justificaciones, `NA`:

```markdown
## Contexto

Para habilitar multi-file por slot había que hacer unos tweaks al modelo y a los templates.

## ¿Qué hay de nuevo?

- [x] Agregué el flag `multi` (default `false`) en `Onboarding::DocumentSlot`
- [x] Eliminé el índice único `(onboarding_step_id, slot_key)` y su validación
- [x] Expuse `documents[]` por slot en dashboard y mantuve `document` por compatibilidad

## Consideraciones
NA
```

Si la validación aporta contexto sobre el comportamiento, la sección opcional puede decir:

```markdown
## Pruebas

- Probé cargar dos documentos en un slot multi. Ambos siguen visibles al recargar.
```

El resultado es ilustrativo; solo incluirlo cuando esa comprobación se haya realizado.

Otro ejemplo, si se verificó mediante tests automatizados: «Reintentar un pago completado conserva un único cobro». Describe la garantía relevante; omite el número de tests, sus archivos y resultados de Sorbet o rubyfmt.

**Esto es demasiado largo** — la justificación y el detalle de campos ya están en el diff:

```markdown
El formulario de onboarding de Chile necesita un paso donde el merchant declara a sus
representantes legales y sube la cédula de identidad de cada uno.

Se reutiliza el modelo `Onboarding::LegalRepresentative` que ya existía para México, pero
Chile pide menos datos: no se piden email ni cargo, y no hay poder notarial por persona.
En su lugar la personería es un único documento del paso completo, y es opcional, porque
los poderes de representación normalmente ya aparecen en la escritura.
```

Debería ser: `El onboarding de Chile necesita un paso para declarar representantes legales y subir su cédula. Reutilicé el modelo de México con menos campos.`
