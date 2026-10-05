
import re

from .ats_analyzer import analyze_ats_score
from .career_analyzer import analyze_career_fit
from .interview_generator import generate_interview_questions
from .job_matcher import compare_resume_to_job_description
from .skill_extractor import extract_skills


def analyze_resume(raw_text, job_description=""):
    text = (raw_text or "").strip()
    if not text:
        return {
            "score": 0,
            "skills": [],
            "missing_skills": [],
            "sections": {},
            "strengths": ["No resume content detected."],
            "suggestions": ["Upload a valid resume with readable text."],
            "roles": [],
            "job_match": {"match_score": 0, "matched_keywords": [], "missing_keywords": []},
            "interview_questions": [],
            "word_count": 0,
        }

    skill_result = extract_skills(text)
    ats_result = analyze_ats_score(text, skill_result["skills"])
    job_match = compare_resume_to_job_description(text, job_description)
    career_fit = analyze_career_fit(text, skill_result["skills"])
    interview_questions = generate_interview_questions(text, skill_result["skills"], career_fit["top_role"])

    resume_score = max(0, min(100, ats_result["score"] * 0.6 + job_match.get("match_score", 0) * 0.25 + career_fit.get("best_match", 0) * 0.15))
    score = round(resume_score, 1)

    strengths = []
    if len(skill_result["skills"]) >= 5:
        strengths.append("Strong technical skill foundation is visible.")
    if ats_result.get("checks", {}).get("experience"):
        strengths.append("There is evidence of work or internship experience.")
    if ats_result.get("checks", {}).get("projects"):
        strengths.append("A projects section adds practical depth to the resume.")
    if ats_result.get("checks", {}).get("contact"):
        strengths.append("Contact information and professional links are included.")
    if not strengths:
        strengths.append("The resume has a solid base but would benefit from clearer structure and stronger content.")

    suggestions = []
    if not ats_result.get("checks", {}).get("summary"):
        suggestions.append("Add a short professional summary tailored to the target job.")
    if not ats_result.get("checks", {}).get("projects"):
        suggestions.append("Highlight 2–3 strong projects with technologies used and measurable outcomes.")
    if not ats_result.get("checks", {}).get("experience"):
        suggestions.append("Include internships, freelance work, or relevant experience to show practical exposure.")
    if not ats_result.get("checks", {}).get("contact"):
        suggestions.append("Add LinkedIn, GitHub, and contact details for recruiter visibility.")
    if skill_result["missing_skills"]:
        suggestions.append("Target the missing skills most aligned with your role and add them to projects or coursework.")
    if not re.search(r"\b(developed|built|implemented|designed|created|tested|deployed|managed|optimized)\b", text.lower()):
        suggestions.append("Use more action-oriented verbs and quantify achievements with numbers and impact.")

    return {
        "score": score,
        "ats_score": ats_result["score"],
        "skills": skill_result["skills"],
        "missing_skills": skill_result["missing_skills"],
        "sections": ats_result["sections"],
        "strengths": strengths,
        "suggestions": suggestions,
        "roles": career_fit["roles"],
        "job_match": {
            "match_score": job_match.get("match_score", 0),
            "matched_keywords": job_match.get("matched_keywords", []),
            "missing_keywords": job_match.get("missing_keywords", []),
            "summary": job_match.get("summary", "")
        },
        "interview_questions": interview_questions,
        "word_count": len((text or "").split()),
        "top_role": career_fit.get("top_role"),
    }
