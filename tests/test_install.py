"""Pruebas del instalador en repos y configuraciones temporales, sin tocar HOME."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agents-install-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo with spaces"
        self.config = self.root / "config"
        self.prepare_repo(self.repo)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        import sys
        fixture = (SOURCE / "tests/fixtures/native_plugin_cli.py").read_text()
        for client in ("codex", "claude"):
            executable = self.bin / client
            executable.write_text(f"#!{sys.executable}\n" + fixture)
            executable.chmod(0o755)

    def prepare_repo(self, repo):
        repo.mkdir(parents=True)
        shutil.copy2(SOURCE / "install.sh", repo / "install.sh")
        shutil.copy2(SOURCE / ".gitignore", repo / ".gitignore")
        shutil.copytree(SOURCE / "hooks", repo / "hooks")
        for name in ("modules", "scripts", ".agents", ".claude-plugin"):
            shutil.copytree(SOURCE / name, repo / name)
        subprocess.run(["git", "init", "-q", str(repo)], check=True)

    def install(self, *args, success=True, repo=None, config=None):
        env = dict(os.environ, AGENT_INSTALL_ROOT=str(config or self.config),
                   PATH=str(self.bin) + os.pathsep + os.environ["PATH"])
        result = subprocess.run(
            ["bash", str((repo or self.repo) / "install.sh"), "--skip-rtk", *args],
            env=env, capture_output=True, text=True,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result

    def write_config(self, relative, text):
        p = self.config / relative
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return p

    def test_native_modules_refresh_without_flat_aliases(self):
        self.install()
        for client in (".codex", ".claude"):
            base = self.config / client / "plugins/cache/work-skills"
            self.assertTrue((base / "personal/1.0.0/skills/code-review/SKILL.md").is_file())
            self.assertTrue((base / "matt-pocock/1.0.0/skills/tdd/SKILL.md").is_file())
            self.assertEqual(len(list(base.glob("*/1.0.0/skills/*/SKILL.md"))), 69)
            self.assertFalse((self.config / client / "skills").exists())
        settings = self.config / ".claude/settings.json"
        before = settings.read_bytes()
        self.install()
        self.assertEqual(before, settings.read_bytes())
        source = self.repo / "modules/personal/skills/code-review/SKILL.md"
        source.write_text(source.read_text() + "\nUpdated skill.\n")
        self.install()
        for client in (".codex", ".claude"):
            installed = self.config / client / "plugins/cache/work-skills/personal/1.0.0/skills/code-review/SKILL.md"
            self.assertEqual(installed.read_bytes(), source.read_bytes())
        self.assertEqual(len(json.loads(settings.read_text())["enabledPlugins"]), 6)

    def test_main_checkout_in_agents_preserves_real_and_synced_skills(self):
        repo = self.config / ".agents"
        self.prepare_repo(repo)
        synced = repo / "skills/synced/provider/custom/SKILL.md"
        synced.parent.mkdir(parents=True)
        synced.write_text("Downloaded skill, not tracked\n")
        claude = self.config / ".claude/skills"
        claude.parent.mkdir()
        claude.symlink_to(repo / "skills")
        self.install(repo=repo)
        self.assertFalse((repo / "skills").is_symlink())
        self.assertEqual(synced.read_text(), "Downloaded skill, not tracked\n")
        self.assertEqual((claude / "synced/provider/custom/SKILL.md").read_text(), synced.read_text())
        self.assertFalse((claude / "code-review").exists())
        for path in [synced, next((repo / "backups").iterdir())]:
            subprocess.run(["git", "-C", str(repo), "check-ignore", "-q", str(path)], check=True)

    def test_migrates_known_adhd_hooks_preserving_other_settings(self):
        keep = {"type": "command", "command": "custom-prompt-hook"}
        rtk = {"type": "command", "command": "rtk hook"}
        settings = {
            "permissions": {"allow": ["Read"]},
            "hooks": {
                "SessionStart": [{"hooks": [{"type": "command", "command": 'sh "/old/i-have-adhd-always-on.sh"'}]}],
                "UserPromptSubmit": [{"hooks": [
                    {"type": "command", "command": "/old/adhd-ruleset-reminder.sh"}, keep]}],
                "PreToolUse": [{"matcher": "Bash", "hooks": [rtk]}],
            },
        }
        p = self.write_config(".claude/settings.json", json.dumps(settings))
        self.write_config(".codex/AGENTS.md", "# Mis reglas\nConservar esta instrucción.\n")
        self.install()
        actual = json.loads(p.read_text())
        self.assertEqual(actual["permissions"], settings["permissions"])
        self.assertEqual(actual["hooks"]["PreToolUse"], settings["hooks"]["PreToolUse"])
        self.assertEqual(actual["hooks"]["UserPromptSubmit"][0], {"hooks": [keep]})
        self.assertEqual(len(actual["hooks"]["UserPromptSubmit"]), 2)
        self.assertEqual(len(actual["hooks"]["SessionStart"]), 1)
        self.assertTrue((self.config / ".codex/AGENTS.md").read_text().startswith("# Mis reglas\nConservar esta instrucción.\n"))
        backups = list((self.config / ".agents/backups").glob("*/claude/settings.json"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(json.loads(backups[0].read_text()), settings)

    def test_on_demand_removes_managed_rules_only(self):
        self.write_config(".codex/AGENTS.md", "Reglas propias\n")
        self.write_config(".claude/settings.json", json.dumps({"hooks": {
            "UserPromptSubmit": [{"hooks": [
                {"type": "command", "command": "/old/adhd-ruleset-reminder.sh"},
                {"type": "command", "command": "own-hook"}]}]}}))
        self.install()
        self.install("--no-adhd-always-on")
        actual = json.loads((self.config / ".claude/settings.json").read_text())
        self.assertNotIn("SessionStart", actual["hooks"])
        self.assertEqual(actual["hooks"]["UserPromptSubmit"][0]["hooks"], [{"type": "command", "command": "own-hook"}])
        self.assertEqual((self.config / ".codex/AGENTS.md").read_text(), "Reglas propias\n")
        self.assertTrue((self.config / ".claude/plugins/cache/work-skills/personal/1.0.0/skills/i-have-adhd/SKILL.md").is_file())

    def test_migrates_quoted_hooks_in_both_modes(self):
        commands = [
            "sh '/old path/adhd-ruleset-reminder.sh'",
            "'/old path/i-have-adhd-always-on.sh'",
            '/bin/bash "/old path/i-have-adhd-always-on.sh"',
            "adhd-ruleset-reminder.sh",
        ]
        for args in [(), ("--no-adhd-always-on",)]:
            with self.subTest(args=args):
                p = self.write_config(".claude/settings.json", json.dumps({"hooks": {
                    "UserPromptSubmit": [{"hooks": [
                        {"type": "command", "command": command} for command in commands
                    ]}]
                }}))
                self.install(*args)
                hooks = json.loads(p.read_text()).get("hooks", {})
                reminders = hooks.get("UserPromptSubmit", [])
                self.assertEqual(len(reminders), 0 if args else 1)
                if reminders:
                    self.assertIn("i-have-adhd-reminder.sh", reminders[0]["hooks"][0]["command"])
                self.assertEqual(len(hooks.get("SessionStart", [])), 0 if args else 1)

    def test_prompt_reminder_is_brief_and_does_not_reactivate_stopped_mode(self):
        self.install()
        settings = json.loads((self.config / ".claude/settings.json").read_text())
        command = settings["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"]
        output = subprocess.check_output(["sh", "-c", command], text=True)
        self.assertIn("stop adhd mode", output)
        self.assertIn("one to three sentences", output)
        self.assertNotIn("ADHD MODE ACTIVE", output)
        self.assertLessEqual(len(output.split()), 90)

        skill = self.repo / "modules/personal/skills/i-have-adhd/SKILL.md"
        text = skill.read_text()
        skill.write_text(text.replace("## Turn reminder\n", "## Turn reminder\nLive rule update.\n"))
        refreshed = subprocess.check_output(["sh", "-c", command], text=True)
        self.assertIn("Live rule update.", refreshed)

    def test_ambiguous_adhd_commands_leave_all_configuration_unchanged(self):
        commands = [
            "/old/adhd-ruleset-reminder.sh && custom-audit-hook",
            "/old/i-have-adhd-reminder.sh && custom-audit-hook",
            "custom-audit-hook; sh '/old path/adhd-ruleset-reminder.sh'",
            "sh '/old path/adhd-ruleset-reminder.sh' | custom-audit-hook",
            "/old/adhd-ruleset-reminder.sh > audit.log",
            'sh "$(custom-audit-hook)/adhd-ruleset-reminder.sh"',
        ]
        for command in commands:
            for args in [(), ("--no-adhd-always-on",)]:
                with self.subTest(command=command, args=args):
                    original = json.dumps({"hooks": {"UserPromptSubmit": [{"hooks": [
                        {"type": "command", "command": command}
                    ]}]}})
                    settings = self.write_config(".claude/settings.json", original)
                    agents = self.write_config(".codex/AGENTS.md", "Mis reglas\n")
                    result = self.install(*args, success=False)
                    self.assertIn("Hook ADHD compuesto o no reconocido", result.stderr)
                    self.assertEqual(settings.read_text(), original)
                    self.assertEqual(agents.read_text(), "Mis reglas\n")
                    self.assertFalse((self.config / ".claude/skills").is_symlink())
                    self.assertFalse((self.config / ".agents").exists())

    def test_relative_root_installs_plugins_and_can_be_reinstalled(self):
        for _ in range(2):
            result = subprocess.run(
                ["bash", str(self.repo / "install.sh"), "--skip-rtk"],
                cwd=self.root, env=dict(os.environ, AGENT_INSTALL_ROOT="relative config", PATH=str(self.bin) + os.pathsep + os.environ["PATH"]),
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            claude = self.root / "relative config/.claude/plugins/cache/work-skills/personal/1.0.0/skills"
            self.assertTrue((claude / "i-have-adhd/SKILL.md").is_file())

    def test_legacy_plugin_flag_is_backed_up_in_both_modes(self):
        for args in [(), ("--no-adhd-always-on",)]:
            with self.subTest(args=args):
                flag = self.write_config(".claude/.i-have-adhd-always", "legacy opt-in\n")
                self.install(*args)
                self.assertFalse(flag.exists())
                backups = list((self.config / ".agents/backups").glob("*/claude/.i-have-adhd-always"))
                self.assertTrue(backups)
                self.assertTrue(all(p.read_text() == "legacy opt-in\n" for p in backups))

    def test_foreign_collections_and_broken_links_are_preserved(self):
        for app in [".agents", ".claude", ".codex"]:
            for kind in ["directory", "symlink", "broken"]:
                with self.subTest(app=app, kind=kind):
                    config = self.root / (app + "-" + kind)
                    path = config / app / "skills"
                    path.parent.mkdir(parents=True)
                    if kind == "directory":
                        path.mkdir()
                        (path / "mine.txt").write_text("keep")
                    else:
                        other = config / "other"
                        if kind == "symlink":
                            other.mkdir()
                            (other / "mine.txt").write_text("keep")
                        path.symlink_to(other)
                    settings = config / ".claude/settings.json"
                    settings.parent.mkdir(exist_ok=True)
                    settings.write_text('{"custom":true}')
                    self.install(config=config)
                    self.assertTrue(json.loads(settings.read_text())["custom"])
                    if kind == "directory":
                        self.assertEqual((path / "mine.txt").read_text(), "keep")
                    else:
                        self.assertEqual(os.readlink(path), str(other))

    def test_incomplete_codex_block_leaves_configuration_unchanged(self):
        settings = self.write_config(".claude/settings.json", '{"custom":true}')
        text = "Mis reglas\n<!-- i-have-adhd:start -->\nContenido sin cierre\n"
        agents = self.write_config(".codex/AGENTS.md", text)
        self.install(success=False)
        self.assertEqual(settings.read_text(), '{"custom":true}')
        self.assertEqual(agents.read_text(), text)
        self.assertFalse((self.config / ".claude/skills").exists())

    def test_invalid_json_leaves_files_unchanged(self):
        settings = self.write_config(".claude/settings.json", '{invalid')
        self.install(success=False)
        self.assertEqual(settings.read_text(), '{invalid')
        self.assertFalse((self.config / ".claude/skills").exists())

    def test_configuration_symlink_is_preserved(self):
        original = self.root / "shared-settings.json"
        original.write_text('{"custom":true}')
        settings = self.config / ".claude/settings.json"
        settings.parent.mkdir(parents=True)
        settings.symlink_to(original)
        self.install()
        self.assertTrue(settings.is_symlink())
        self.assertTrue(json.loads(original.read_text())["custom"])

    def test_legacy_folder_links_are_backed_up_without_losing_foreign_skills(self):
        old = self.repo / "skills"
        shutil.copytree(self.repo / "modules/personal/skills/code-review", old / "code-review")
        foreign = old / "synced/custom/SKILL.md"
        foreign.parent.mkdir(parents=True)
        foreign.write_text("Foreign skill\n")
        for app in (".agents", ".claude"):
            link = self.config / app / "skills"
            link.parent.mkdir(parents=True)
            link.symlink_to(old)
        self.install()
        for app in (".agents", ".claude"):
            directory = self.config / app / "skills"
            self.assertFalse(directory.is_symlink())
            self.assertFalse((directory / "code-review").exists())
            self.assertEqual((directory / "synced/custom/SKILL.md").read_text(), "Foreign skill\n")
        backups = list((self.config / ".agents/backups").glob("*/agents/skills-root"))
        self.assertEqual(len(backups), 1)
        self.assertTrue(backups[0].is_symlink())
        self.assertTrue((old / "code-review/SKILL.md").is_file())

    def test_legacy_individual_and_stable_snapshot_links_are_backed_up(self):
        old = self.repo / "skills/code-review"
        shutil.copytree(self.repo / "modules/personal/skills/code-review", old)
        snapshot = self.root / "snapshot"
        imported = snapshot / "skills/spec-driven-development"
        shutil.copytree(self.repo / "modules/addyosmani/skills/spec-driven-development", imported)
        (snapshot / "source.json").write_text(json.dumps({"source": "https://github.com/addyosmani/agent-skills"}))
        directory = self.config / ".codex/skills"
        directory.mkdir(parents=True)
        for source in (old, imported):
            (directory / source.name).symlink_to(source)
        foreign = directory / "foreign"
        foreign.symlink_to(self.root / "missing")
        self.install()
        self.assertEqual(list(directory.iterdir()), [foreign])
        self.assertTrue(old.is_dir())
        self.assertTrue(imported.is_dir())
        backups = list((self.config / ".agents/backups").glob("*/codex/skills/*"))
        self.assertEqual({p.name for p in backups}, {"code-review", "spec-driven-development"})

    def test_native_failure_preserves_legacy_aliases(self):
        from unittest.mock import patch
        old = self.repo / "skills"
        old.mkdir()
        link = self.config / ".agents/skills"
        link.parent.mkdir(parents=True)
        link.symlink_to(old)
        with patch.dict(os.environ, {"AGENT_TEST_FAIL_PLUGIN": "matt-pocock"}):
            self.install(success=False)
        self.assertTrue(link.is_symlink())

    def test_other_marketplace_with_same_name_is_not_replaced(self):
        for client in (".codex", ".claude"):
            with self.subTest(client=client):
                config = self.root / (client + "-marketplace")
                registry = config / client / "plugins/known_marketplaces.json"
                registry.parent.mkdir(parents=True)
                original = {"work-skills": {"source": {"source": "directory", "path": str(self.root / "another-repo")}}}
                registry.write_text(json.dumps(original))
                result = self.install(config=config, success=False)
                self.assertIn("otra colección", result.stderr)
                self.assertEqual(json.loads(registry.read_text()), original)

    def test_same_collection_can_move_between_checkouts(self):
        old = self.root / "previous-checkout"
        self.prepare_repo(old)
        remote = "https://github.com/example/agent-collection.git"
        for repo in (old, self.repo):
            subprocess.run(["git", "-C", str(repo), "remote", "add", "origin", remote], check=True)
        self.install(repo=old)
        self.install()
        for client in (".codex", ".claude"):
            registry = self.config / client / "plugins/known_marketplaces.json"
            self.assertEqual(Path(json.loads(registry.read_text())["work-skills"]["source"]["path"]).resolve(), self.repo.resolve())
        saved = list((self.config / ".agents/backups").glob("*/claude/plugins/known_marketplaces.json"))
        self.assertTrue(any(Path(json.loads(p.read_text())["work-skills"]["source"]["path"]).resolve() == old.resolve() for p in saved))

    def test_modules_are_self_contained_and_keep_original_skill_names(self):
        import re
        for module in (SOURCE / "modules").iterdir():
            manifest = json.loads((module / "plugin.json").read_text())
            adapter = json.loads((module / ".claude-plugin/plugin.json").read_text())
            self.assertEqual({k: v for k, v in manifest.items() if k != "$schema"}, adapter)
            for skill in (module / "skills").iterdir():
                text = (skill / "SKILL.md").read_text()
                self.assertIn("\nname: " + skill.name + "\n", text)
                for markdown in skill.rglob("*.md"):
                    for path in re.findall(r"(?:\.\./)+references/[a-z-]+\.md|(?<![\w/])references/[a-z-]+\.md", markdown.read_text()):
                        target = (markdown.parent / path).resolve()
                        self.assertTrue(target.is_file(), str(target))
                        self.assertTrue(target.is_relative_to(module.resolve()))

    def test_worktree_installation_is_rejected(self):
        subprocess.run(["git", "-C", str(self.repo), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.repo), "-c", "user.name=Installer Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture"], check=True)
        worktree = self.root / "worktree"
        subprocess.run(["git", "-C", str(self.repo), "worktree", "add", "--detach", str(worktree)], check=True, capture_output=True)
        result = self.install(repo=worktree, success=False)
        self.assertIn("worktree temporal", result.stderr)
        self.assertFalse(self.config.exists())

    def test_isolated_root_requires_skip_rtk(self):
        result = subprocess.run(["bash", str(self.repo / "install.sh")], env=dict(os.environ, AGENT_INSTALL_ROOT=str(self.config)), capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.config.exists())


if __name__ == "__main__":
    unittest.main()
