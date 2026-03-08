"""
Helper to load Deep Agent skills from a directory.

Handles Windows path compatibility by using native Python Path operations
instead of POSIX paths, avoiding issues with DeepAgents' internal path handling.
"""

import yaml
from pathlib import Path
from typing import List
from deepagents import SubAgent, CompiledSubAgent


def load_skills_from_dir(skills_dir: Path) -> List[SubAgent | CompiledSubAgent]:
    """
    Load skills from a directory and convert them to SubAgent format.

    This function scans for SKILL.md files, parses their YAML frontmatter,
    and returns SubAgent dicts that can be passed to create_deep_agent().

    Using this approach (instead of passing skills= parameter) avoids
    Windows path handling issues in DeepAgents' internal skill loading.

    Args:
        skills_dir: Path to directory containing skill subdirectories

    Returns:
        List of SubAgent TypedDicts ready for create_deep_agent()

    Example:
        skills_dir = Path(__file__).parent / "skills"
        skills = load_skills_from_dir(skills_dir)
        agent = create_deep_agent(model=llm, subagents=skills, ...)
    """
    if not skills_dir.exists():
        return []

    subagents = []

    # Scan for skill directories
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        # Parse skill file
        try:
            skill = _parse_skill_file(skill_file, skill_dir.name)
            subagent = _skill_to_subagent(skill)
            subagents.append(subagent)
        except Exception as e:
            # Skip skills that fail to load
            print(f"Warning: Failed to load skill '{skill_dir.name}': {e}")

    return subagents


def _parse_skill_file(skill_file: Path, skill_name: str) -> dict:
    """Parse SKILL.md file and extract metadata and content."""
    content = skill_file.read_text(encoding="utf-8")

    # Check for YAML frontmatter
    metadata = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            # parts[0] is empty, parts[1] is frontmatter, parts[2] is body
            frontmatter_str = parts[1].strip()
            body = parts[2].strip()

            try:
                metadata = yaml.safe_load(frontmatter_str) or {}
            except yaml.YAMLError:
                # If YAML parsing fails, treat as plain content
                metadata = {}
                body = content

    return {
        "name": metadata.get("name", skill_name),
        "description": metadata.get("description", ""),
        "content": body,
        "model": metadata.get("model"),  # Optional model override
    }


def _skill_to_subagent(skill: dict) -> SubAgent:
    """Convert parsed skill dict to DeepAgents SubAgent TypedDict."""
    subagent: SubAgent = {
        "name": skill["name"],
        "description": skill["description"] or f"Skill: {skill['name']}",
        "system_prompt": skill["content"],
    }

    # Add model override if specified
    if skill["model"]:
        subagent["model"] = skill["model"]

    return subagent
