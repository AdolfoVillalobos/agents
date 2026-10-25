# Módulo addyosmani

## Usar en este y otros dispositivos

1. Sincroniza esta versión del repo y ejecuta `make install` desde su checkout principal. `make install-no-rtk` omite RTK.
2. Abre una sesión nueva. En Claude Code, prueba `/addyosmani:spec-driven-development`. En Codex, selecciona `addyosmani:spec-driven-development` en el menú de skills.

El plugin registra las 25 skills bajo `addyosmani:<nombre>`. También puedes pedir que el agente lea `modules/addyosmani/skills/spec-driven-development/SKILL.md` de este checkout. [Catálogo completo](catalog.md#colección-de-addy-osmani) y [opciones de instalación](portability.md#instalación).

## Procedencia y recursos

- Origen: [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills).
- Versión importada: [`aeac41d4d005999432bb7312f7ff06383a91d59d`](https://github.com/addyosmani/agent-skills/commit/aeac41d4d005999432bb7312f7ff06383a91d59d).
- `modules/addyosmani/skills/` conserva el contenido original, incluidos nombres, scripts y referencias internas. Cada skill añade la licencia MIT original en `LICENSE.txt`.
- Los siete documentos compartidos viven en `modules/addyosmani/references/`. Viajan dentro del plugin y conservan sus rutas relativas y otra copia de la licencia.
- `.skill-lock.json` usa claves `addyosmani:<nombre>`. Registra el commit de origen, su ruta original y la ruta local. `skillFolderHash` representa el árbol Git original, antes de añadir la copia local de la licencia.

## Alcance

El módulo incluye las skills y sus referencias. Los comandos abreviados `/spec`, `/build` o `/ship`, hooks y personas del plugin original requieren aquella integración; no se registran aquí. Invoca los nombres cualificados completos. `doubt-driven-development` permite un subagente genérico según sus instrucciones, sin registrar sus personas opcionales de `agents/`.

Las instrucciones conservan su estado importado: algunas requieren herramientas concretas o subagentes. `browser-testing-with-devtools` requiere Chrome DevTools MCP. El inicializador opcional de `idea-refine` se invoca con la ruta real de su script desde el proyecto donde quieras crear `docs/ideas/`.

La comprobación de instalación, integridad e inventario de skills no equivale a ejecutar sus workflows con modelos ni a validar su comportamiento entre proveedores.
