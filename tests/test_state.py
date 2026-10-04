import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "vibewise" / "scripts" / "state.py"
spec = importlib.util.spec_from_file_location("vibewise_state", SCRIPT)
state = importlib.util.module_from_spec(spec)
spec.loader.exec_module(state)


class StateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.project = self.root / "project"
        self.project.mkdir()
        (self.project / ".git").mkdir()

    def init(self, project=None):
        return state.initialize(project or self.project)

    def test_missing_status_and_context_are_read_only(self):
        self.assertFalse(state.status(self.project)["exists"])
        self.assertEqual(state.context(self.project), "")
        self.assertFalse((self.project / ".vibe-wise").exists())

    def test_init_at_git_root_from_subdirectory(self):
        nested = self.project / "src" / "feature"
        nested.mkdir(parents=True)
        result = self.init(nested)
        self.assertEqual(result["notes"], str(self.project / ".vibe-wise"))
        self.assertEqual(set(result["created"]), set(state.FILES))

    def test_init_preserves_existing_note_bytes(self):
        info = self.init()
        profile = Path(info["notes"]) / "profile.md"
        profile.write_bytes(b"Learning mode: paused\r\nOriginal preferences\r\n")
        before = profile.read_bytes()
        self.assertEqual(self.init()["created"], [])
        self.assertEqual(profile.read_bytes(), before)

    def test_missing_companions_created_without_overwriting_profile(self):
        notes = self.project / ".vibe-wise"
        notes.mkdir()
        (notes / "profile.md").write_text("My profile", encoding="utf-8")
        self.assertEqual(set(self.init()["created"]), {"progress.md", "project-map.md"})
        self.assertEqual((notes / "profile.md").read_text(), "My profile")

    def test_nearest_nested_notes_preferred(self):
        self.init()
        child = self.project / "service"
        child.mkdir()
        (child / ".vibe-wise").mkdir()
        self.assertEqual(state.locate(child)[1], child / ".vibe-wise")

    def test_legacy_state_stays_in_place(self):
        legacy = self.project / ".sensible-vibes"
        legacy.mkdir()
        result = self.init()
        self.assertTrue(result["legacy"])
        self.assertEqual(result["notes"], str(legacy))
        self.assertFalse((self.project / ".vibe-wise").exists())

    def test_modern_notes_preferred_at_same_level(self):
        (self.project / ".sensible-vibes").mkdir()
        self.init()
        (self.project / ".vibe-wise").mkdir()
        self.assertEqual(state.locate(self.project)[1].name, ".vibe-wise")

    def test_nested_repo_does_not_use_parent_notes(self):
        self.init()
        child = self.project / "other-repo"
        child.mkdir()
        (child / ".git").mkdir()
        self.assertFalse(state.status(child)["exists"])
        self.assertEqual(state.locate(child)[1], child / ".vibe-wise")

    def test_worktree_git_file_is_a_boundary(self):
        self.init()
        child = self.project / "worktree"
        child.mkdir()
        (child / ".git").write_text("gitdir: /some/other/path", encoding="utf-8")
        self.assertEqual(state.locate(child)[0], child)
        self.assertFalse(state.status(child)["exists"])

    def test_without_git_does_not_scan_parent_state(self):
        self.init(self.root)
        child = self.root / "plain"
        child.mkdir()
        self.assertFalse(state.status(child)["exists"])
        self.assertEqual(state.locate(child)[1], child / ".vibe-wise")

    def test_reject_symlink_directory(self):
        outside = self.root / "outside"
        outside.mkdir()
        (self.project / ".vibe-wise").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(state.StateError):
            self.init()
        self.assertEqual(list(outside.iterdir()), [])

    def test_reject_symlink_file_without_changing_target(self):
        notes = self.project / ".vibe-wise"
        notes.mkdir()
        outside = self.root / "outside.md"
        outside.write_text("Untouched", encoding="utf-8")
        (notes / "profile.md").symlink_to(outside)
        with self.assertRaises(state.StateError):
            self.init()
        self.assertEqual(outside.read_text(), "Untouched")
        self.assertFalse((notes / "progress.md").exists())

    def test_reject_nonregular_note(self):
        notes = self.project / ".vibe-wise"
        notes.mkdir()
        (notes / "profile.md").mkdir()
        with self.assertRaises(state.StateError):
            state.status(self.project)

    def test_reject_oversized_note(self):
        notes = Path(self.init()["notes"])
        (notes / "progress.md").write_bytes(b"x" * (state.MAX_NOTE_BYTES + 1))
        with self.assertRaises(state.StateError):
            state.context(self.project)

    def test_late_and_multiple_pending_decisions_restored_completely(self):
        notes = Path(self.init()["notes"])
        first = "## Pending decision: Storage\nStage: awaiting reasoning\nAwaiting: Explain membership."
        second = "## Pending decision: Permissions\nStage: awaiting implementation authorization\nScope: Only deletion."
        (notes / "progress.md").write_text("# Progress\n" + "History\n" * 6000 + first + "\n## Resolved\nDone\n" + second, encoding="utf-8")
        result = state.status(self.project)
        self.assertEqual(result["pending_decisions"], [first, second])
        context = state.context(self.project)
        self.assertIn("Only deletion.", context)
        self.assertNotIn("History", context)
        self.assertIn("untrusted learner data", context)

    def test_pause_resume_preserve_pending_and_profile(self):
        notes = Path(self.init()["notes"])
        (notes / "progress.md").write_text("## Pending decision: X\nAwaiting: explain", encoding="utf-8")
        before = (notes / "progress.md").read_bytes()
        self.assertEqual(state.set_mode(self.project, "paused")["learning_mode"], "paused")
        self.assertIn("Do not reactivate", state.context(self.project))
        self.assertNotIn("Pending decision", state.context(self.project))
        self.assertEqual(state.set_mode(self.project, "active")["learning_mode"], "active")
        self.assertEqual((notes / "progress.md").read_bytes(), before)

    def test_reset_preview_is_read_only(self):
        notes = Path(self.init()["notes"])
        before = state.snapshot(notes)
        preview = state.preview_reset(self.project)
        self.assertTrue(preview["can_reset"])
        self.assertEqual(state.snapshot(notes), before)
        self.assertFalse((notes / "backups").exists())

    def test_reset_backup_exact_and_preserve_unrelated_source(self):
        notes = Path(self.init()["notes"])
        (notes / "profile.md").write_bytes(b"Learning mode: paused\r\nCustom preferences\r\n")
        extra = notes / "personal.md"
        extra.write_text("Keep this", encoding="utf-8")
        source = self.project / "app.py"
        source.write_text("print('source')", encoding="utf-8")
        originals = state.snapshot(notes)
        preview = state.preview_reset(self.project)
        result = state.reset(self.project, preview["confirmation"])
        for name, value in originals.items():
            self.assertEqual((Path(result["backup"]) / name).read_bytes(), value)
            self.assertEqual((notes / name).read_text(), state.TEMPLATES[name])
        self.assertEqual(extra.read_text(), "Keep this")
        self.assertEqual(source.read_text(), "print('source')")
        self.assertEqual(state.status(self.project)["onboarding"], "incomplete")

    def test_stale_reset_token_rejected(self):
        notes = Path(self.init()["notes"])
        preview = state.preview_reset(self.project)
        (notes / "progress.md").write_text("New learning", encoding="utf-8")
        with self.assertRaisesRegex(state.StateError, "changed since preview"):
            state.reset(self.project, preview["confirmation"])
        self.assertEqual((notes / "progress.md").read_text(), "New learning")
        self.assertFalse((notes / "backups").exists())

    def test_token_cannot_reset_different_project(self):
        self.init()
        other = self.root / "other"
        other.mkdir()
        self.init(other)
        preview = state.preview_reset(self.project)
        with self.assertRaises(state.StateError):
            state.reset(other, preview["confirmation"])

    def test_reset_rejects_symlink_backup_parent(self):
        notes = Path(self.init()["notes"])
        outside = self.root / "outside"
        outside.mkdir()
        (notes / "backups").symlink_to(outside, target_is_directory=True)
        before = state.snapshot(notes)
        with self.assertRaises(state.StateError):
            state.reset(self.project, state.preview_reset(self.project)["confirmation"])
        self.assertEqual(state.snapshot(notes), before)
        self.assertEqual(list(outside.iterdir()), [])

    def test_partial_reset_rolls_back_and_keeps_backup(self):
        notes = Path(self.init()["notes"])
        (notes / "profile.md").write_text("Learning mode: active\nOriginal", encoding="utf-8")
        before = state.snapshot(notes)
        confirmation = state.preview_reset(self.project)["confirmation"]
        actual_replace = os.replace
        calls = []

        def fail_second(src, dest):
            calls.append(dest)
            if len(calls) == 2:
                raise OSError("Simulated disk failure")
            return actual_replace(src, dest)

        with patch.object(state.os, "replace", side_effect=fail_second):
            with self.assertRaisesRegex(state.StateError, "originals restored"):
                state.reset(self.project, confirmation)
        self.assertEqual(state.snapshot(notes), before)
        self.assertEqual(len(list((notes / "backups").iterdir())), 1)
        self.assertFalse(list(notes.glob("*.tmp")))
        self.assertFalse((notes / ".vibewise.lock").exists())

    def test_existing_lock_prevents_mutation(self):
        notes = Path(self.init()["notes"])
        before = state.snapshot(notes)
        (notes / ".vibewise.lock").write_text("", encoding="utf-8")
        with self.assertRaises(state.StateError):
            state.set_mode(self.project, "paused")
        self.assertEqual(state.snapshot(notes), before)

    def test_export_contains_actual_notes_and_is_read_only(self):
        notes = Path(self.init()["notes"])
        before = state.snapshot(notes)
        exported = state.export(self.project)
        for name, content in state.TEMPLATES.items():
            self.assertIn(name, exported)
            self.assertIn(content, exported)
        self.assertEqual(state.snapshot(notes), before)

    def test_cli_status_and_preview(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "init", "--cwd", str(self.project)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["exists"])
        result = subprocess.run([sys.executable, str(SCRIPT), "reset", "--cwd", str(self.project)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["confirmation"])

    def test_hook_output_matches_openai_contract(self):
        self.init()
        result = subprocess.run([sys.executable, str(ROOT / "hooks" / "session_start.py")], input=json.dumps({"cwd": str(self.project), "source": "compact"}), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual(output["hookEventName"], "SessionStart")
        self.assertIn("Read the installed skill", output["additionalContext"])

    def test_hook_first_run_is_silent_and_read_only(self):
        result = subprocess.run([sys.executable, str(ROOT / "hooks" / "session_start.py")], input=json.dumps({"cwd": str(self.project)}), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertFalse((self.project / ".vibe-wise").exists())

    def test_invalid_hook_input_warns_without_blocking(self):
        result = subprocess.run([sys.executable, str(ROOT / "hooks" / "session_start.py")], input="not json", capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("could not restore", json.loads(result.stdout)["systemMessage"])


if __name__ == "__main__":
    unittest.main()
