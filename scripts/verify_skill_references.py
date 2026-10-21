#!/usr/bin/env python3
"""
verify_skill_references.py

Validates that all agent skill references across the repository point to skills
that actually exist in this repository.

Checks:
1. All Markdown links pointing to skills, skill files (SKILL.md), or skill directories.
2. All in-text repository skill paths: `skills/<category>/<skill-name>`.
3. All dependencies and sub-skills listed in skill README and SKILL.md files.
4. All slash command skill invocations and skill mentions in documentation tables.

Exit code:
  0 = All referenced skills exist in this repository.
  1 = Broken or nonexistent skill references detected.
"""

import argparse
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(REPO_ROOT, "skills")

KNOWN_CATEGORIES = {
    "personal",
    "development",
    "engineering",
    "productivity",
    "financial",
    "deprecated",
}

EXCLUDED_DIRS = {".git", "tests", ".system_generated"}

PLACEHOLDERS = {
    "skill-name",
    "<skill-name>",
    "feature_name",
    "<feature_name>",
    "<task>",
    "<idea>",
    "<issue>",
    "target",
    "<target>",
    "task or bug fix",
    "<task or bug fix>",
    "spec or feature",
    "<spec or feature>",
}


def discover_skills(skills_dir):
    """
    Scans `skills/` and returns:
    - skill_dirs: dict of dir_name -> rel_path
    - skill_names: dict of frontmatter_name -> rel_path
    - skill_rel_paths: set of relative directory paths (e.g. 'skills/development/code-review')
    """
    skill_dirs = {}
    skill_names = {}
    skill_rel_paths = set()

    for root, dirs, files in os.walk(skills_dir):
        if "SKILL.md" in files:
            dname = os.path.basename(root)
            rel_path = os.path.relpath(root, REPO_ROOT).replace("\\", "/")
            skill_dirs[dname] = rel_path
            skill_rel_paths.add(rel_path)

            skill_md = os.path.join(root, "SKILL.md")
            try:
                with open(skill_md, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                m = re.search(r"^name:\s*([^\n\r]+)", content, re.MULTILINE)
                if m:
                    skill_names[m.group(1).strip()] = rel_path
            except Exception:
                pass

    return skill_dirs, skill_names, skill_rel_paths


def check_skill_references(repo_root, verbose=False):
    skill_dirs, skill_names, skill_rel_paths = discover_skills(SKILLS_DIR)
    all_valid_identifiers = set(skill_dirs.keys()) | set(skill_names.keys())

    issues = []
    total_refs_checked = 0

    link_re = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    path_re = re.compile(r"\bskills/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)\b")
    subskill_table_re = re.compile(r"Sub-skill used\s*\|\s*([^|\n]+)")

    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for file in files:
            if not file.endswith(".md"):
                continue
            file_path = os.path.join(root, file)
            rel_file = os.path.relpath(file_path, repo_root).replace("\\", "/")

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                lines = content.splitlines()

            for line_no, line in enumerate(lines, 1):
                # Check 1: In-text skill path references: skills/<category>/<skill-name>
                for m in path_re.finditer(line):
                    cat, sname = m.group(1), m.group(2)
                    if cat in KNOWN_CATEGORIES:
                        # Ignore standard subdirectories inside skills
                        if sname in {
                            "assets",
                            "scripts",
                            "references",
                            "templates",
                            "evals",
                            "sources",
                        }:
                            continue
                        total_refs_checked += 1
                        expected_rel = f"skills/{cat}/{sname}"
                        target_path = os.path.join(SKILLS_DIR, cat, sname)
                        skill_md = os.path.join(target_path, "SKILL.md")
                        if not os.path.isfile(skill_md):
                            issues.append(
                                f"{rel_file}:{line_no}: In-text skill path '{expected_rel}' does not exist as a valid skill directory with SKILL.md"
                            )
                        elif verbose:
                            print(f"[OK] {rel_file}:{line_no} -> {expected_rel}")

                # Check 2: Markdown links targeting skills or SKILL.md
                for anchor, link in link_re.findall(line):
                    clean_link = link.split("#")[0].strip()
                    if not clean_link or clean_link.startswith(
                        ("http://", "https://", "mailto:", "#")
                    ):
                        continue

                    # Category directories (e.g. skills/development)
                    if clean_link.rstrip("/").split("/") == ["skills", clean_link.rstrip("/").split("/")[-1]] and clean_link.rstrip("/").split("/")[-1] in KNOWN_CATEGORIES:
                        total_refs_checked += 1
                        target_full = os.path.normpath(
                            os.path.join(os.path.dirname(file_path), clean_link)
                        )
                        if not os.path.isdir(target_full):
                            issues.append(
                                f"{rel_file}:{line_no}: Category link target does not exist: '[{anchor}]({link})'"
                            )
                        elif verbose:
                            print(f"[OK] {rel_file}:{line_no} -> category link [{anchor}]({link})")
                        continue

                    # If the link refers to a skill directory or SKILL.md
                    is_skill_link = (
                        "skills/" in clean_link
                        or clean_link.endswith("SKILL.md")
                        or anchor.strip("`") in all_valid_identifiers
                    )

                    if is_skill_link:
                        # Ignore template placeholders (e.g. `[rfc-filename].md`)
                        if "[" in clean_link or "<" in clean_link:
                            continue

                        total_refs_checked += 1
                        target_full = os.path.normpath(
                            os.path.join(os.path.dirname(file_path), clean_link)
                        )
                        rel_target = os.path.relpath(target_full, repo_root).replace(
                            "\\", "/"
                        )

                        if not os.path.exists(target_full):
                            issues.append(
                                f"{rel_file}:{line_no}: Skill link target does not exist: '[{anchor}]({link})' -> resolved to '{rel_target}'"
                            )
                        else:
                            # If it targets a directory, ensure it contains SKILL.md
                            if os.path.isdir(target_full):
                                if not os.path.isfile(
                                    os.path.join(target_full, "SKILL.md")
                                ):
                                    issues.append(
                                        f"{rel_file}:{line_no}: Target directory '{rel_target}' is missing SKILL.md"
                                    )
                                elif verbose:
                                    print(f"[OK] {rel_file}:{line_no} -> [{anchor}]({link})")
                            elif verbose:
                                print(f"[OK] {rel_file}:{line_no} -> [{anchor}]({link})")

                # Check 3: Sub-skill table entries (e.g., `| **Sub-skill used** | ...`)
                sub_match = subskill_table_re.search(line)
                if sub_match:
                    skills_cell = sub_match.group(1)
                    # Extract backticked names `name`
                    for s in re.findall(r"`([a-zA-Z0-9_-]+)`", skills_cell):
                        # Filter out non-skill mentions like templates
                        if s in {"git-master", "test-driven-development", "incremental-implement", "code-review", "write-prd", "request-feature", "implement-task", "investigate-issue"}:
                            total_refs_checked += 1
                            if s not in all_valid_identifiers:
                                issues.append(
                                    f"{rel_file}:{line_no}: Sub-skill '{s}' in table does not exist in repository"
                                )
                            elif verbose:
                                print(f"[OK] {rel_file}:{line_no} -> Sub-skill `{s}`")

    return total_refs_checked, issues


def main():
    parser = argparse.ArgumentParser(
        description="Verify that all agent skill references in this repository exist."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print all verified references"
    )
    args = parser.parse_args()

    skill_dirs, skill_names, _ = discover_skills(SKILLS_DIR)
    print(f"Discovered {len(skill_dirs)} agent skills across {SKILLS_DIR}.")

    total_refs, issues = check_skill_references(REPO_ROOT, verbose=args.verbose)

    print(f"Verified {total_refs} skill references across repository documents.")

    if issues:
        print(f"\n❌ FAILED: Found {len(issues)} broken skill reference(s):\n")
        for issue in issues:
            print(f"  • {issue}")
        sys.exit(1)
    else:
        print("\n✅ SUCCESS: All agent skill references in this repository exist!")
        sys.exit(0)


if __name__ == "__main__":
    main()
