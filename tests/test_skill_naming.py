import os
import re
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(REPO_ROOT, "skills")

RENAMED_SKILLS = [
    "implement-task",
    "incremental-implement",
    "investigate-issue",
    "request-feature",
    "write-prd",
]

DEPRECATED_SKILL_NAMES = [
    "implement_task",
    "incremental_implement",
    "investigate_issue",
    "request_feature",
    "write_prd",
]

KEBAB_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def get_all_skills():
    """Returns a list of tuples: (skill_name, skill_dir, skill_md_path, content)."""
    skills = []
    for root, dirs, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            skill_md_path = os.path.join(root, "SKILL.md")
            skill_dir = os.path.basename(root)
            with open(skill_md_path, "r", encoding="utf-8") as f:
                content = f.read()
            m = re.search(r"^name:\s*([^\n\r]+)", content, re.MULTILINE)
            name = m.group(1).strip() if m else None
            skills.append((name, skill_dir, skill_md_path, content))
    return skills


class TestSkillNamingConventions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skills = get_all_skills()

    def test_no_underscore_in_skill_directories(self):
        """Verify that every skill directory name adheres to kebab-case and contains no underscore."""
        violations = []
        for name, skill_dir, path, _ in self.skills:
            if "_" in skill_dir:
                violations.append(f"Directory contains underscore: {skill_dir} at {path}")
            if not KEBAB_PATTERN.match(skill_dir):
                violations.append(f"Directory not kebab-case: {skill_dir} at {path}")

        self.assertEqual(
            violations,
            [],
            f"Found skill directories with invalid naming:\n" + "\n".join(violations),
        )

    def test_frontmatter_name_no_underscore(self):
        """Verify that SKILL.md frontmatter 'name' contains no underscore across all skills."""
        violations = []
        for name, skill_dir, path, _ in self.skills:
            self.assertIsNotNone(name, f"Missing 'name' field in {path}")
            if "_" in name:
                violations.append(f"Skill name contains underscore: '{name}' in {path}")
            if not KEBAB_PATTERN.match(name):
                violations.append(f"Skill name is not valid kebab-case: '{name}' in {path}")

        self.assertEqual(
            violations,
            [],
            f"Found frontmatter naming violations:\n" + "\n".join(violations),
        )

    def test_renamed_skills_directories_and_frontmatter_match(self):
        """Verify that all 5 target skills exist with kebab-case directory and matching frontmatter name."""
        skill_dict = {s[1]: s[0] for s in self.skills}
        for target in RENAMED_SKILLS:
            self.assertIn(
                target,
                skill_dict,
                f"Renamed skill directory '{target}' not found in skills/development/",
            )
            self.assertEqual(
                skill_dict[target],
                target,
                f"Frontmatter name for '{target}' does not match directory name",
            )

    def test_no_stale_deprecated_skill_references(self):
        """Verify that no deprecated underscore skill names exist anywhere in repo markdown files."""
        violations = []
        excluded_dirs = {".git", "tests"}
        pattern = re.compile(
            r"\b(" + "|".join(re.escape(k) for k in DEPRECATED_SKILL_NAMES) + r")\b"
        )

        for root, dirs, files in os.walk(REPO_ROOT):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, REPO_ROOT)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        for line_num, line in enumerate(f, 1):
                            matches = pattern.findall(line)
                            if matches:
                                violations.append(
                                    f"{rel_path}:{line_num}: Found deprecated reference(s): {matches}"
                                )

        self.assertEqual(
            violations,
            [],
            f"Found stale underscore skill references:\n" + "\n".join(violations),
        )

    def test_renamed_skills_markdown_links_resolve(self):
        """Verify that all markdown references to the 5 renamed skills point to valid paths."""
        link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
        broken_links = []

        for root, dirs, files in os.walk(REPO_ROOT):
            if ".git" in root or "tests" in root:
                continue
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    rel_source = os.path.relpath(file_path, REPO_ROOT)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    for text, link in link_pattern.findall(content):
                        # Only check links that mention any of the renamed skills
                        if any(skill in link for skill in RENAMED_SKILLS):
                            clean_link = link.split("#")[0]
                            target_path = os.path.normpath(
                                os.path.join(os.path.dirname(file_path), clean_link)
                            )
                            if not os.path.exists(target_path):
                                broken_links.append(
                                    f"{rel_source} -> broken link '{link}' (resolved to {target_path})"
                                )

        self.assertEqual(
            broken_links,
            [],
            f"Found broken skill links:\n" + "\n".join(broken_links),
        )


if __name__ == "__main__":
    unittest.main()
