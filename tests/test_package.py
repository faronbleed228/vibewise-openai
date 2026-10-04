import importlib.util
import json
from pathlib import Path
import re
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("vibewise_build", ROOT / "scripts" / "build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class PackageTests(unittest.TestCase):
    def test_shared_chatgpt_pack_is_current_and_portable(self):
        build.build(check=True)
        self.assertLessEqual(len(build.chat_instructions()), 8000)

    def test_plugin_paths_and_skill_resources_resolve(self):
        manifest = json.loads((ROOT / "plugin.json").read_text())
        self.assertEqual(manifest["license"], "MIT")
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
        hook_path = manifest["extensions"]["com.openai"]["hooks"]
        self.assertTrue((ROOT / hook_path).is_file())
        skill = ROOT / "skills" / "vibewise" / "SKILL.md"
        content = skill.read_text()
        header = content.split("---", 2)[1]
        self.assertIn("name: vibewise\n", header)
        self.assertRegex(header, r"\ndescription: \S.+")
        for link in re.findall(r"\]\(([^)]+)\)", content):
            self.assertTrue((skill.parent / link).is_file(), link)
        metadata = (skill.parent / "agents" / "openai.yaml").read_text()
        self.assertIn("$vibewise", metadata)
        self.assertNotIn("allow_implicit_invocation: false", metadata)

    def test_hook_command_resolves_to_bundled_helper(self):
        config = json.loads((ROOT / "hooks" / "hooks.json").read_text())
        handler = config["hooks"]["SessionStart"][0]["hooks"][0]
        self.assertIn('"${PLUGIN_ROOT}/hooks/session_start.py"', handler["command"])
        self.assertTrue((ROOT / "hooks" / "session_start.py").is_file())

    def test_bundles_contain_runtime_and_license_without_local_notes(self):
        bundles = build.build()
        plugin = next(p for p in bundles if p.name == "vibewise-openai.zip")
        with zipfile.ZipFile(plugin) as archive:
            names = set(archive.namelist())
            for name in ("plugin.json", "LICENSE", "NOTICE.md", "hooks/session_start.py", "skills/vibewise/scripts/state.py", "chatgpt/instructions.md", "scripts/build.py", "tests/test_state.py"):
                self.assertIn(name, names)
            self.assertFalse(any("__pycache__" in p or ".vibe-wise/" in p for p in names))
            catalog = json.loads(archive.read(".agents/plugins/marketplace.json"))
            entry = catalog["plugins"][0]
            self.assertEqual(entry["source"]["path"], "./")
            self.assertIn("policy", entry)
            self.assertEqual(entry["name"], json.loads(archive.read("plugin.json"))["name"])
        chat = next(p for p in bundles if p.name == "vibewise-chatgpt.zip")
        with zipfile.ZipFile(chat) as archive:
            self.assertIn("chatgpt/instructions.md", archive.namelist())
            self.assertIn("LICENSE", archive.namelist())
            self.assertNotIn("plugin.json", archive.namelist())


if __name__ == "__main__":
    unittest.main()
