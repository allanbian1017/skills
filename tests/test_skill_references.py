import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.verify_skill_references import check_skill_references, discover_skills, SKILLS_DIR


class TestSkillReferencesExist(unittest.TestCase):
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
