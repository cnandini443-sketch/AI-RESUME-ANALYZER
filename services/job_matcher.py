import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STOPWORDS_FILE = BASE_DIR / "data" / "stopwords.json"


with open(STOPWORDS_FILE, "r", encoding="utf-8") as file:
    STOPWORDS = set(json.load(file))


def _extract_keywords(text):
    text = (text or "").lower()
    tokens = re.findall(r"[a-z0-9+#./-]+", text)
    valid = []
    for token in tokens:
        token = token.strip(".,;:()[]{}\"'")
        if len(token) < 3:
            continue
        if token in STOPWORDS:
            continue
        valid.append(token)
    unique = []
    seen = set()
    for token in valid:
        if token not in seen:
            unique.append(token)
            seen.add(token)
    return unique


def compare_resume_to_job_description(resume_text, job_description):
    job_text = (job_description or "").strip()
    if not job_text:
        return {
            "match_score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "summary": "Paste a job description to compare your resume against the role requirements.",
        }

    resume_keywords = set(_extract_keywords(resume_text))
    jd_keywords = set(_extract_keywords(job_text))
    matched_keywords = sorted(resume_keywords & jd_keywords)
    missing_keywords = sorted(jd_keywords - resume_keywords)

    match_score = round((len(matched_keywords) / max(len(jd_keywords), 1)) * 100) if jd_keywords else 0
    if match_score >= 80:
        summary = "Strong alignment with the role requirements. Your experience covers most key qualifications."
    elif match_score >= 60:
        summary = "Good role match. You are close to the target profile and can strengthen a few requirements."
    elif match_score >= 40:
        summary = "Partial match. Add some missing role-specific keywords, accomplishments, and project evidence."
    else:
        summary = "Low match. Your resume needs clearer role targeting and more alignment with the job requirements."

    return {
        "match_score": match_score,
        "matched_keywords": matched_keywords[:12],
        "missing_keywords": missing_keywords[:12],
        "summary": summary,
    }
