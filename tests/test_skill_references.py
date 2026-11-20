import os
import sys
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.verify_skill_references import check_skill_references, discover_skills, SKILLS_DIR


class TestSkillReferencesExist(unittest.TestCase):
    def test_external_skill_links_do_not_hide_broken_local_paths(self):
        """External dependency links are allowed; local paths must still exist."""
        with TemporaryDirectory() as directory:
            document = Path(directory) / "README.md"
            document.write_text(
                "[git-master](https://github.com/allanbian1017/dep-skills/"
                "blob/main/skills/development/git-master/SKILL.md)\n"
                "Install from `../dep-skills/skills/development/git-master`\n"
            )
            _, issues = check_skill_references(directory)
            self.assertEqual(issues, [])

            with document.open("a") as stream:
                stream.write("Missing local `skills/development/missing-skill`\n")
            _, issues = check_skill_references(directory)
            self.assertEqual(len(issues), 1)
            self.assertIn("skills/development/missing-skill", issues[0])

    def test_all_agent_skill_references_exist(self):
        """Verify that every skill reference across all repository markdown files points to an existing skill."""
        skill_dirs, _, _ = discover_skills(SKILLS_DIR)
        self.assertGreater(len(skill_dirs), 0, "No skills discovered in skills directory")

        total_checked, issues = check_skill_references(REPO_ROOT, verbose=False)
        self.assertGreater(total_checked, 0, "No skill references were checked")
        self.assertEqual(
            issues,
            [],
            f"Found {len(issues)} broken or nonexistent skill reference(s):\n"
            + "\n".join(f"  • {issue}" for issue in issues),
        )


if __name__ == "__main__":
    unittest.main()
