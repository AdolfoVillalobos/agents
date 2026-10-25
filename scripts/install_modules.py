#!/usr/bin/env python3
"""Instala los módulos nativos y respalda los accesos planos de esta colección."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess


def origin(repo):
    result = subprocess.run(
        ["git", "-C", str(repo), "config", "--get", "remote.origin.url"],
        capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def migration_plan(repo, roots, names, backup):
    """Identifica enlaces propios antes de modificar cualquiera de sus destinos."""
    repo_origin = origin(repo)

    def owned_root(path):
        path = path.resolve()
        return path == repo / "skills" or (
            path.name == "skills" and repo_origin is not None
            and origin(path.parent) == repo_origin
        )

    def owned_entry(entry):
        if not entry.is_symlink() or entry.name not in names:
            return False
        target = entry.resolve()
        if target.name == entry.name and owned_root(target.parent):
            return True
        # Instalación estable de Addy creada antes de introducir los módulos.
        receipt = target.parent.parent / "source.json"
        if target.name != entry.name or not receipt.is_file():
            return False
        try:
            source = json.loads(receipt.read_text())
        except (ValueError, OSError):
            return False
        skill = names[entry.name]
        return (
            source.get("source") == "https://github.com/addyosmani/agent-skills"
            and skill.parts[-3] == "addyosmani"
            and (target / "SKILL.md").is_file()
            and (target / "SKILL.md").read_bytes() == (skill / "SKILL.md").read_bytes()
        )

    plan = []
    for app, root in roots.items():
        directory = root / "skills"
        if directory.is_symlink():
            if owned_root(directory):
                keep = [(p.name, p.resolve()) for p in directory.iterdir()
                        if p.name not in names] if directory.exists() else []
                plan.append((directory, backup / app / "skills-root", keep))
        elif directory.is_dir():
            for entry in directory.iterdir():
                if owned_entry(entry):
                    plan.append((entry, backup / app / "skills" / entry.name, None))
    return plan


def install(repo, roots, backup, check=False):
    catalog = json.loads((repo / ".agents/plugins/marketplace.json").read_text())
    marketplace = catalog["name"]
    names = {}
    for entry in catalog["plugins"]:
        package = (repo / entry["source"]["path"]).resolve()
        package.relative_to(repo)
        manifest = json.loads((package / "plugin.json").read_text())
        if manifest["name"] != entry["name"]:
            raise ValueError(f"Módulo inconsistente: {package}")
        for skill in (package / "skills").iterdir():
            if (skill / "SKILL.md").is_file():
                names[skill.name] = skill

    clients = [name for name in ("codex", "claude") if shutil.which(name)]
    if not clients:
        raise ValueError("Instala Codex o Claude Code antes de registrar los módulos.")
    env = dict(os.environ, CODEX_HOME=str(roots["codex"]),
               CLAUDE_CONFIG_DIR=str(roots["claude"]))
    repo_origin = origin(repo)
    previous = {}
    if "codex" in clients and roots["codex"].exists():
        result = subprocess.run(["codex", "plugin", "marketplace", "list", "--json"],
                                env=env, capture_output=True, text=True, check=True)
        for registered_market in json.loads(result.stdout)["marketplaces"]:
            if registered_market["name"] == marketplace:
                path = Path(registered_market["root"]).resolve()
                if path != repo:
                    if repo_origin is None or origin(path) != repo_origin:
                        raise ValueError(f"El marketplace {marketplace} de Codex apunta a otra colección. Se conservó.")
                    previous["codex"] = path
    # No sustituye otro marketplace que casualmente tenga el mismo nombre.
    registry = roots["claude"] / "plugins/known_marketplaces.json"
    known = json.loads(registry.read_text()) if registry.is_file() else {}
    registered = known.get(marketplace)
    if "claude" in clients and registered:
        source = registered.get("source", {})
        path = Path(source.get("path", "")).resolve()
        if source.get("source") != "directory" or (path != repo and (repo_origin is None or origin(path) != repo_origin)):
            raise ValueError(f"El marketplace {marketplace} de Claude apunta a otra colección. Se conservó.")
        if path != repo:
            previous["claude"] = path

    plan = migration_plan(repo, roots, names, backup)
    if check:
        return
    for client in clients:
        roots[client].mkdir(parents=True, exist_ok=True)
        if client in previous:
            subprocess.run([client, "plugin", "marketplace", "remove", marketplace], env=env, check=True)
        if client == "codex" or not registered or client in previous:
            subprocess.run([client, "plugin", "marketplace", "add", str(repo)], env=env, check=True)
        for entry in catalog["plugins"]:
            verb = "add" if client == "codex" else "install"
            subprocess.run([client, "plugin", verb, f'{entry["name"]}@{marketplace}'], env=env, check=True)

    # Retira los alias solo después de instalar todos los módulos correctamente.
    for path, destination, keep in plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), str(destination))
        if keep is not None:
            path.mkdir()
            for name, target in keep:
                (path / name).symlink_to(target, target_is_directory=target.is_dir())
    print(f'Módulos registrados en {", ".join(clients)}. Accesos antiguos respaldados: {len(plan)}.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--agents-dir", required=True, type=Path)
    parser.add_argument("--claude-dir", required=True, type=Path)
    parser.add_argument("--codex-dir", required=True, type=Path)
    parser.add_argument("--backup", type=Path, default=Path("unused"))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        install(args.repo.resolve(), {"agents": args.agents_dir, "claude": args.claude_dir,
                "codex": args.codex_dir}, args.backup, args.check)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"No se completó la instalación de módulos: {error}\n")
