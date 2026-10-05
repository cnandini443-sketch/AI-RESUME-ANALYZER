import random


def generate_interview_questions(resume_text, skills, role_name="Software Engineer"):
    skill_list = (skills or [])[:5]
    if not skill_list:
        skill_list = ["Python", "problem solving", "communication", "teamwork"]

    role_name = role_name or "Software Engineer"
    questions = [
        f"Tell me about a project where you used {skill_list[0]} to solve a real-world problem.",
        f"Describe a time you collaborated with a team to deliver a feature or solution using {', '.join(skill_list[1:3])}.",
        f"How would you explain your experience in {role_name} to a recruiter in under 2 minutes?",
        "What trade-offs did you consider when choosing a technology stack for one of your projects?",
        "How do you handle feedback on your work and how do you improve based on it?",
        "What would you build next to strengthen your portfolio for this role?",
    ]
    return questions[:5]
