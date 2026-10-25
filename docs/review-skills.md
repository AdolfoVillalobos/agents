# Revisiones especializadas

Tres puntos de entrada para pedir una revisión concreta, y uno para redactar los comentarios, sin reemplazar `code-review`:

| Petición | Skill | Resultado |
| --- | --- | --- |
| «Revisa el diseño de esta PR» | `review-design` | Problemas de estructura y simplificaciones justificadas, sin editar |
| «Busca bugs recorriendo los flujos» | `review-qa` | Regresiones verificadas por ejecución o trazado, con sus límites |
| «¿Está lista para merge y despliegue?» | `review-readiness` | Decisión condicionada a intención, compatibilidad y riesgo operativo |
| «Déjame los comentarios para pegar» | `review-comments` | Borradores anclados a la línea, a partir de hallazgos que ya sobrevivieron |

Para un pase completo se pueden pedir las tres primeras, secuencialmente sobre el mismo alcance, y después `review-comments` si hacen falta borradores. No se requieren agentes paralelos. La rúbrica compartida vive en `modules/personal/skills/code-review/references/review-protocol.md`; el comportamiento de la skill general `code-review` no cambia.

Mientras estos archivos estén solo en un worktree, evalúalos por su ruta explícita. Por ejemplo: «Lee `modules/personal/skills/review-qa/SKILL.md` de este checkout y úsala para revisar el repositorio indicado contra su base real». La instalación global puede contener otra versión. Las dependencias entre carpetas están descritas en [portabilidad](portability.md).

## Procedencia y decisiones

Adaptación de los documentos aportados por el usuario el 2026-10-07:

- `pr-review-prompts-listos.md`: prompts A, B y C y rúbrica compartida D.
- `pr-review-prompts.md`: investigación, motivaciones, antipatrones y contexto de esos prompts.

La investigación aportada atribuye ideas a Google Engineering Practices, Conventional Comments, los prompts públicos de revisión de OpenAI y Anthropic, y el contrato de PR de Addy Osmani. Esta adaptación toma los documentos entregados como material de diseño; no representa una nueva verificación de sus afirmaciones sobre versiones, flags, número de agentes o capacidades de productos. Esos detalles no se incorporan a las instrucciones.

Cambios deliberados al convertir los prompts en skills:

- Alcance determinado por la PR o el repositorio, incluyendo bases apiladas y trabajo local cuando corresponde. No se presupone `upstream/main` ni se mezclan cambios locales con una PR remota sin pedirlo.
- Confianza acompañada de evidencia y contraargumentos; el número no es una probabilidad calibrada. Severidad según impacto y alcance, sin equivalencia automática entre `blocker` y P0.
- Rúbrica compartida y referencia condicional de pagos. Se conserva la representación monetaria del repositorio, sin imponer enteros o decimales universalmente.
- Descripciones breves en español, sin referencias a issues ni atribuciones a proveedores; pruebas centradas en comportamiento. Una descripción pobre no constituye por sí sola un defecto bloqueante.
- Se omiten plantillas vacías, conteos de hallazgos descartados, elogios obligatorios y tres mejoras forzosas. La revisión puede terminar sin hallazgos.

## Comentarios para pegar

`review-comments` adapta el paquete `pr-review-assist` y el brief de comentarios aportados el 2026-10-13. El brief recoge Conventional Comments, las guías de Google y GitLab, y la mecánica de líneas y sugerencias de GitHub. Esta adaptación usa esos documentos como material de diseño. No vuelve a verificar sus afirmaciones sobre productos, límites numéricos de la industria ni taxonomías P0–P3.

Entra el formato del comentario: ancla en una línea del diff, etiqueta que dice si bloquea, fence `suggestion` solo para un reemplazo exacto, nits agrupados, elogio solo cuando es concreto, y borrador en el idioma del PR con una nota privada aparte. Publicar sigue pidiendo autorización.

Queda fuera lo que ya cubre otra skill o ata la colección a un equipo: las tres lentes de investigación, el checklist de pagos, los modos `personal` y `work`, la inferencia por el remote, y las instrucciones de instalación.

Los casos están en [evaluacion.md](../modules/personal/skills/review-comments/evaluacion.md). Validación estructural; evaluación con modelos pendiente.

## Casos de evaluación

Estos casos son contratos de comportamiento para futuras ejecuciones, no resultados obtenidos con un modelo. Para cada ejecución, registrar skill y revisión exactas, alcance, modelo, comandos, respuesta y resultado observado. Entregar al evaluador el prompt y los archivos del caso sin anticipar la respuesta esperada.

### Diseño

| Prompt y material del caso | Resultado esperado |
| --- | --- |
| «Revisa el diseño». El diff agrega un wrapper que únicamente renombra una llamada existente, sin contrato propio; hay un patrón directo equivalente en el mismo paquete. | Propone simplificar con ubicaciones y beneficio concreto; no lo convierte en un fallo de producción ni edita código. |
| «Revisa el diseño». Un wrapper con un solo consumidor aplica aislamiento de tenant y una transacción requerida. | No propone borrarlo solo por tener un consumidor; verifica la garantía y los llamadores. |
| «¿Sobran tests?». Dos tests parecidos cubren límites distintos; otro duplica exactamente la misma condición y aserción. | Conserva los límites distintos y justifica únicamente la duplicación real, identificando cobertura retenida. |

### QA

| Prompt y material del caso | Resultado esperado |
| --- | --- |
| «Busca bugs». Un webhook nuevo aplica dos veces un efecto ante replay; el caso incluye entrada repetida y almacenamiento local sin deduplicación. | Traza el efecto repetido, comprueba guardas y aporta repro o razonamiento preciso; no inventa que ejecutó un test. |
| Mismo aspecto del webhook, pero una restricción persistente y su manejo transaccional garantizan un único efecto. | Descarta el falso positivo después de leer la restricción y la frontera del efecto. |
| «Revisa esta PR». El fallo sospechado ya existe sin cambios en la base. | No lo presenta como regresión introducida por la PR. |
| «Revisa el bugfix». Los tests mockean la frontera que contiene el bug y pasan también sin el arreglo. | Describe el fallo concreto no detectado y el nivel de prueba adecuado; no pide simplemente más tests. |
| La suite exige un servicio local que no está disponible. | Registra la limitación, distingue trazado de ejecución y no usa servicios productivos como sustituto. |

### Preparación para merge

| Prompt y material del caso | Resultado esperado |
| --- | --- |
| «¿Podemos desplegar?». Una migración elimina una columna que la versión anterior todavía lee; despliegue gradual sin compatibilidad. | Expone el fallo durante coexistencia y rollback, con referencias; un flag de aplicación no basta para declarar seguro el cambio. |
| Cambio acotado y verificado, descripción genérica sin contexto útil. | Propone cuerpo breve en español con hechos comprobados; no bloquea automáticamente por la prosa ni exige inventario de autoría IA. |
| Issue enlazado inaccesible, pero contrato técnico verificable en el repositorio. | Declara el límite de cobertura de intención y continúa; no inventa requisitos ni bloquea por falta de acceso al tracker. |

### Alcance y entrega

| Prompt y material del caso | Resultado esperado |
| --- | --- |
| PR apilada contra una rama padre, más un archivo local ajeno. | Usa base/head reales y excluye el archivo local de la revisión de esa PR. |
| «Revisa mi trabajo actual», con cambios comprometidos, staged, unstaged y un archivo nuevo relevante. | Incluye y distingue las cuatro fuentes, sin llamar revisión completa a un diff solo de HEAD. |
| «Vuelve a revisar» tras corregir el hallazgo; aparecen preferencias de nombres en código intacto. | Comprueba la corrección y cambios afectados; no añade nits ajenos al cambio. |
| «Ejecuta los tres pases». Dos pases detectan la misma causa raíz. | Reporta una vez la causa, conserva fallos independientes y no dice que hubo revisores independientes si trabajó secuencialmente. |

## Validación de esta entrega

Se comprobaron frontmatter y nombres con Ruby/YAML, referencias relativas con Python y limpieza del diff con Git. El validador `quick_validate.py` no pudo ejecutarse por falta de PyYAML; se usaron esas comprobaciones alternativas sin instalar dependencias globales. Estos controles verifican estructura y empaquetado; no miden precisión de hallazgos ni adherencia del modelo. Queda pendiente ejecutar los casos con Claude y Codex en repositorios de prueba.
