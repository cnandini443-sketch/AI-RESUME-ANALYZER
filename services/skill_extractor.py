import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SKILLS_FILE = BASE_DIR / "data" / "skills.json"


def _normalize_skill_name(skill):
    return re.sub(r"\s+", " ", str(skill)).strip()


def _skill_matches(resume_text, skill_name):
    text = (resume_text or "").lower()
    skill = _normalize_skill_name(skill_name).lower()
    if not skill:
        return False

    if skill in {"c", "c++"}:
        patterns = [r"\bc\b", r"\bc\+\+\b"]
    else:
        patterns = [re.escape(skill)]

    if any(re.search(pattern, text) for pattern in patterns):
        return True

    alternatives = {
        "react": ["react.js", "reactjs"],
        "node.js": ["nodejs", "node.js"],
        "rest api": ["rest-api", "rest api", "api"],
        "artificial intelligence": ["ai"],
        "machine learning": ["ml"],
        "scikit-learn": ["sklearn"],
        "google cloud": ["gcp"],
        "mysql": ["my sql"],
    }
    for alias in alternatives.get(skill, []):
        if re.search(rf"\b{re.escape(alias)}\b", text):
            return True

    return False


def extract_skills(resume_text):
    with open(SKILLS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    known_skills = []
    skill_map = {}
    for item in data.get("skills", []):
        if isinstance(item, dict):
            skill_name = item.get("name")
            category = item.get("category", "General")
        else:
            skill_name = item
            category = "General"

        skill_name = _normalize_skill_name(skill_name)
        if not skill_name:
            continue

        known_skills.append(skill_name)
        skill_map.setdefault(category, []).append(skill_name)

    found = []
    categories = {}
    for category, skills in skill_map.items():
        matched = []
        for skill in skills:
            if _skill_matches(resume_text, skill):
                matched.append(skill)
        if matched:
            categories[category] = matched
            found.extend(matched)

    seen = set()
    ordered_skills = []
    for skill in found:
        if skill not in seen:
            ordered_skills.append(skill)
            seen.add(skill)

    recommended = [
        _normalize_skill_name(skill)
        for skill in data.get("recommended_skills", [])
    ]
    missing_skills = [skill for skill in recommended if skill not in ordered_skills][:12]
    soft_skills = [
        _normalize_skill_name(skill)
        for skill in data.get("soft_skills", [])
        if _skill_matches(resume_text, skill)
    ]

    return {
        "skills": ordered_skills,
        "categories": categories,
        "missing_skills": missing_skills,
        "soft_skills": soft_skills,
    }
