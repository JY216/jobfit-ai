SKILL_ALIASES = {
    "spring": "spring boot",
    "springboot": "spring boot",
    "spring boot": "spring boot",

    "postgres": "postgresql",
    "postgresql": "postgresql",

    "js": "javascript",
    "javascript": "javascript",

    "react.js": "react",
    "reactjs": "react",
    "react": "react",

    "aws": "aws",
    "amazon web services": "aws",

    "fast api": "fastapi",
    "fastapi": "fastapi",
}


def normalize_skill(skill: str) -> str:
    normalized = skill.strip().lower()

    return SKILL_ALIASES.get(normalized, normalized)


def match_skills(
    candidate_skills: list[str],
    required_skills: list[str]
) -> tuple[list[str], list[str]]:

    candidate_set = {
        normalize_skill(skill)
        for skill in candidate_skills
    }

    required_set = {
        normalize_skill(skill)
        for skill in required_skills
    }

    matched = required_set & candidate_set
    missing = required_set - candidate_set

    return sorted(matched), sorted(missing)
