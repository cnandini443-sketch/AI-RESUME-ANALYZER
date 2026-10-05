import re

ACTION_VERBS = [
    "built",
    "developed",
    "designed",
    "implemented",
    "created",
    "managed",
    "improved",
    "optimized",
    "automated",
    "analyzed",
    "delivered",
    "maintained",
    "deployed",
    "tested",
]


def analyze_ats_score(text, skills):
    text = text or ""
    lowered = text.lower()

    sections = {
        "summary": bool(re.search(r"\b(summary|profile|objective|about me)\b", lowered)),
        "education": bool(re.search(r"\b(education|degree|b\.tech|bachelor|master|university|college)\b", lowered)),
        "experience": bool(re.search(r"\b(experience|internship|work history|career|professional experience)\b", lowered)),
        "projects": bool(re.search(r"\b(projects?|portfolio|case study)\b", lowered)),
        "skills": bool(re.search(r"\b(skills|technical skills|tools|technologies)\b", lowered) or bool(skills)),
        "contact": bool(re.search(r"(linkedin|github|portfolio|@\w+|\+?\d[\d\s-]{8,})", lowered)),
    }

    action_count = len(re.findall(r"\b(" + "|".join(ACTION_VERBS) + r")\b", lowered))
    skill_density = 1 if skills else 0
    keyword_score = min(1, len(skills) / 8) if skills else 0
    length_score = 1 if 150 <= len(text.split()) <= 1200 else 0.6 if len(text.split()) >= 75 else 0.2

    total_score = (
        (sum(sections.values()) / len(sections)) * 35
        + keyword_score * 25
        + (1 if action_count >= 3 else 0.4 if action_count >= 1 else 0) * 15
        + length_score * 20
        + (1 if sections["contact"] else 0) * 5
    )

    score = max(0, min(100, round(total_score, 1)))
    issues = []
    for section_name, present in sections.items():
        if not present and section_name != "skills":
            issues.append(f"Add a clear {section_name} section to improve ATS readability.")

    if action_count < 3:
        issues.append("Use stronger action verbs and measurable outcomes in your bullet points.")

    if len(skills) < 5:
        issues.append("Add more technical and role-specific keywords to strengthen ATS matching.")

    return {
        "score": score,
        "checks": sections,
        "sections": sections,
        "issues": issues,
    }
