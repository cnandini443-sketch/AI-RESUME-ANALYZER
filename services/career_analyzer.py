import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ROLES_FILE = BASE_DIR / "data" / "job_roles.json"

with open(ROLES_FILE, "r", encoding="utf-8") as file:
    ROLE_DATA = json.load(file)


def _normalize_skill(skill):
    return str(skill).strip().lower()


def analyze_career_fit(resume_text, skills):
    text = (resume_text or "").lower()
    skill_set = {_normalize_skill(skill) for skill in skills}

    roles = []
    for role in ROLE_DATA:
        required_skills = [_normalize_skill(skill) for skill in role.get("skills", [])]
        matched = [skill for skill in required_skills if skill in skill_set]
        missing = [skill for skill in required_skills if skill not in skill_set]
        match_pct = round((len(matched) / len(required_skills)) * 100) if required_skills else 0
        roles.append({
            "role": role.get("role", "Role"),
            "description": role.get("description", ""),
            "match": match_pct,
            "matched": matched,
            "skill_gap": missing,
        })

    roles.sort(key=lambda item: item["match"], reverse=True)
    top_role = roles[0]["role"] if roles else "Generalist"
    best_match = roles[0]["match"] if roles else 0

    recommended = []
    for item in roles[:3]:
        for skill in item["skill_gap"][:2]:
            recommended.append(skill)

    return {
        "top_role": top_role,
        "best_match": best_match,
        "roles": roles[:5],
        "recommended_skills": recommended[:8],
    }
