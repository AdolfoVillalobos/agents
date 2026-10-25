"""Doble de los CLI nativos. No ejecuta agentes ni usa configuración personal."""
import json
import os
from pathlib import Path
import shutil
import sys

client = Path(sys.argv[0]).name
config = Path(os.environ["CODEX_HOME" if client == "codex" else "CLAUDE_CONFIG_DIR"])
args = sys.argv[1:]
config.mkdir(parents=True, exist_ok=True)
registry = config / "plugins/known_marketplaces.json"
known = json.loads(registry.read_text()) if registry.exists() else {}

if args[:3] == ["plugin", "marketplace", "list"]:
    print(json.dumps({"marketplaces": [{"name": name, "root": data["source"]["path"]}
                                      for name, data in known.items()]}))
elif args[:3] == ["plugin", "marketplace", "remove"]:
    del known[args[3]]
    registry.write_text(json.dumps(known))
elif args[:3] == ["plugin", "marketplace", "add"]:
    root = Path(args[3])
    catalog = json.loads((root / ".claude-plugin/marketplace.json").read_text())
    known[catalog["name"]] = {"source": {"source": "directory", "path": str(root)}}
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(json.dumps(known))
elif args[:2] in (["plugin", "add"], ["plugin", "install"]):
    module, marketplace = args[2].split("@")
    if os.environ.get("AGENT_TEST_FAIL_PLUGIN") == module:
        sys.exit("Falla nativa simulada")
    root = Path(known[marketplace]["source"]["path"])
    catalog = json.loads((root / ".claude-plugin/marketplace.json").read_text())
    entry = next(p for p in catalog["plugins"] if p["name"] == module)
    source = root / entry["source"]
    manifest = json.loads((source / "plugin.json").read_text())
    dest = config / "plugins/cache" / marketplace / module / manifest["version"]
    shutil.copytree(source, dest, dirs_exist_ok=True)
    if client == "claude":
        settings = config / "settings.json"
        data = json.loads(settings.read_text()) if settings.exists() else {}
        data.setdefault("enabledPlugins", {})[args[2]] = True
        settings.write_text(json.dumps(data, indent=2))
else:
    sys.exit(f"Comando no cubierto por el doble nativo: {args}")
