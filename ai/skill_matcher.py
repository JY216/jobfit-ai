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

SKILL_RELATIONS = {
    "rdbms": {
        "postgresql",
        "mysql",
        "mariadb",
        "oracle",
        "sql server",
    }
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

    matched = []
    missing = []

    for required_skill in required_set:
        # 1. 기술명이 직접 일치하는 경우
        if required_skill in candidate_set:
            matched.append(required_skill)
            continue

        # 2. 상위 기술 요구사항을 구체 기술로 충족하는 경우
        related_skills = SKILL_RELATIONS.get(required_skill, set())

        if candidate_set & related_skills:
            matched.append(required_skill)
            continue

        # 3. 둘 다 아니라면 미충족
        missing.append(required_skill)

    return sorted(matched), sorted(missing)

def calculate_skill_score(
    candidate_skills: list[str],
    required_skills: list[str],
    preferred_skills: list[str]
) -> dict:
    required_matched, required_missing = match_skills(
        candidate_skills,
        required_skills
    )

    preferred_matched, preferred_missing = match_skills(
        candidate_skills,
        preferred_skills
    )

    required_rate = (
        len(required_matched) / len(required_skills)
        if required_skills else 1.0
    )

    preferred_rate = (
        len(preferred_matched) / len(preferred_skills)
        if preferred_skills else 1.0
    )

    # 필수 기술 80%, 우대 기술 20%
    skill_score = round(
        (required_rate * 80) +
        (preferred_rate * 20)
    )

    return {
        "score": skill_score,
        "required_match_rate": round(required_rate * 100),
        "preferred_match_rate": round(preferred_rate * 100),
        "required_matched": required_matched,
        "required_missing": required_missing,
        "preferred_matched": preferred_matched,
        "preferred_missing": preferred_missing,
    }

def calculate_jobfit_score(
    skill_score: int,
    experience_score: int
) -> dict:
    # 1차 기준: 기술 적합도 70%, 경험 적합도 30%
    skill_weight = 0.7
    experience_weight = 0.3

    final_score = round(
        (skill_score * skill_weight) +
        (experience_score * experience_weight)
    )

    return {
        "final_score": final_score,
        "skill_score": skill_score,
        "experience_score": experience_score,
        "weights": {
            "skill": 70,
            "experience": 30
        }
    }