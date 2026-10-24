# Skills de Addy Osmani

## Usar en este y otros dispositivos

1. Incorpora esta importación al checkout principal del repo y sincronízalo en el otro dispositivo.
2. Desde ese checkout, ejecuta `make install`. Usa `make install-no-rtk` para omitir RTK. El instalador requiere `jq` y se detiene si encuentra otra colección en los destinos; [detalles y conservación de instalaciones existentes](portability.md#instalación).
3. Abre una sesión nueva del agente. Prueba `$spec-driven-development` en Codex o `/spec-driven-development` en Claude Code.

Para usar esta versión explícitamente en un workspace, pide:

```text
Lee skills/spec-driven-development/SKILL.md de este checkout
y úsala para especificar <cambio>.
```

El repo contiene las 25 skills y sus recursos: después de obtener estos cambios, instalarlas en otro dispositivo no requiere volver a descargar la colección original. [Catálogo completo](catalog.md#colección-de-addy-osmani).

## Procedencia y archivos

- Origen: [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills).
- Versión importada: [`aeac41d4d005999432bb7312f7ff06383a91d59d`](https://github.com/addyosmani/agent-skills/commit/aeac41d4d005999432bb7312f7ff06383a91d59d).
- Las carpetas `skills/<nombre>/` conservan el contenido original, incluidos scripts y referencias internas. Cada una añade `LICENSE.txt`, con la licencia MIT original de Addy Osmani.
- Los siete documentos de `references/` conservan su ubicación relativa a `skills/` y su propia copia de la licencia. Traslada ambas carpetas juntas; copiar solo `SKILL.md` pierde recursos.
- `.skill-lock.json` registra el origen, commit y árbol Git original de cada skill. El hash representa la carpeta de origen antes de añadir `LICENSE.txt`; no es una comprobación de todas las adaptaciones locales ni habilita actualizaciones automáticas.

## Alcance de la importación

Se instalan las skills y sus referencias. Los comandos `/spec`, `/build` o `/ship`, hooks y personas del plugin original requieren su integración nativa; no se registran aquí. Invoca las skills por sus nombres completos. `doubt-driven-development` puede usar un subagente genérico según sus propias instrucciones; la colección no registra las personas opcionales mencionadas en `agents/`.

Las instrucciones originales siguen como importadas: algunas dependen de herramientas concretas, solicitan aprobación o requieren subagentes. `browser-testing-with-devtools` requiere Chrome DevTools MCP. El inicializador opcional de `idea-refine` se invoca mediante la ruta real de su `scripts/idea-refine.sh`, desde el proyecto donde quieras crear `docs/ideas/`.

Esta incorporación conserva las instrucciones de origen. Las comprobaciones de formato, integridad de archivos, rutas de recursos e instalación aislada no equivalen a ejecutar los workflows con modelos ni a validar comportamiento entre proveedores.
