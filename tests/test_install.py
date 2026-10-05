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

    def prepare_repo(self, repo):
        repo.mkdir(parents=True)
        shutil.copy2(SOURCE / "install.sh", repo / "install.sh")
        shutil.copy2(SOURCE / ".gitignore", repo / ".gitignore")
        shutil.copytree(SOURCE / "hooks", repo / "hooks")
        shutil.copytree(SOURCE / "skills/i-have-adhd", repo / "skills/i-have-adhd")
        subprocess.run(["git", "init", "-q", str(repo)], check=True)

    def install(self, *args, success=True, repo=None, config=None):
        env = dict(os.environ, AGENT_INSTALL_ROOT=str(config or self.config))
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

    def test_whole_folder_shares_new_skills_and_is_idempotent(self):
        self.install()
        agents = self.config / ".agents/skills"
        claude = self.config / ".claude/skills"
        self.assertTrue(agents.is_symlink())
        self.assertEqual(os.readlink(claude), str(agents))
        self.assertEqual(claude.resolve(), (self.repo / "skills").resolve())
        new = self.repo / "skills/new-skill"
        new.mkdir()
        (new / "SKILL.md").write_text("New skill\n")
        self.assertEqual((claude / "new-skill/SKILL.md").read_text(), "New skill\n")
        paths = [self.config / ".claude/settings.json", self.config / ".codex/AGENTS.md"]
        before = [p.read_bytes() for p in paths]
        self.install()
        self.assertEqual(before, [p.read_bytes() for p in paths])
        settings = json.loads(paths[0].read_text())
        hook = settings["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        output = subprocess.check_output(["sh", "-c", hook], text=True)
        self.assertIn("ADHD MODE ACTIVE", output)
        self.assertNotIn("disable-model-invocation:", output)

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
        self.assertEqual(os.readlink(claude), str(repo / "skills"))
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
        self.assertEqual(actual["hooks"]["UserPromptSubmit"], [{"hooks": [keep]}])
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
        self.assertTrue((self.config / ".claude/skills/i-have-adhd/SKILL.md").is_file())

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
                self.assertNotIn("UserPromptSubmit", hooks)
                self.assertEqual(len(hooks.get("SessionStart", [])), 0 if args else 1)

    def test_ambiguous_adhd_commands_leave_all_configuration_unchanged(self):
        commands = [
            "/old/adhd-ruleset-reminder.sh && custom-audit-hook",
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

    def test_relative_root_creates_working_links_and_can_be_reinstalled(self):
        for _ in range(2):
            result = subprocess.run(
                ["bash", str(self.repo / "install.sh"), "--skip-rtk"],
                cwd=self.root, env=dict(os.environ, AGENT_INSTALL_ROOT="relative config"),
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            claude = self.root / "relative config/.claude/skills"
            self.assertTrue((claude / "i-have-adhd/SKILL.md").is_file())
            self.assertEqual(claude.resolve(), (self.repo / "skills").resolve())

    def test_legacy_plugin_flag_is_backed_up_in_both_modes(self):
        for args in [(), ("--no-adhd-always-on",)]:
            with self.subTest(args=args):
                flag = self.write_config(".claude/.i-have-adhd-always", "legacy opt-in\n")
                self.install(*args)
                self.assertFalse(flag.exists())
                backups = list((self.config / ".agents/backups").glob("*/claude/.i-have-adhd-always"))
                self.assertTrue(backups)
                self.assertTrue(all(p.read_text() == "legacy opt-in\n" for p in backups))

    def test_foreign_collections_and_broken_links_are_not_replaced(self):
        for app in [".agents", ".claude"]:
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
                    result = self.install(config=config, success=False)
                    self.assertIn("otra colección", result.stderr)
                    self.assertEqual(settings.read_text(), '{"custom":true}')
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
