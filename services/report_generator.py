from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, ListFlowable

BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_FOLDER = BASE_DIR / "reports"


def generate_report_pdf(analysis):
    REPORTS_FOLDER.mkdir(exist_ok=True)
    analysis_id = analysis.get("id", "resume")
    output_path = REPORTS_FOLDER / f"resume_report_{analysis_id}.pdf"

    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    result = analysis.get("details", analysis) if isinstance(analysis, dict) else {}
    score = result.get("score", analysis.get("score", 0))
    ats = result.get("ats_score", analysis.get("ats_score", 0))
    match_score = result.get("job_match", {}).get("match_score", analysis.get("match_score", 0))

    story.append(Paragraph("AI Resume Analyzer Report", styles["Title"]))
    story.append(Spacer(1, 16))
    story.append(Paragraph(f"Candidate: {analysis.get('filename', 'Resume')}"))
    story.append(Paragraph(f"Overall Score: {score}/100"))
    story.append(Paragraph(f"ATS Score: {ats}/100"))
    story.append(Paragraph(f"Job Match: {match_score}%"))
    story.append(Spacer(1, 12))

    key_sections = [
        ("Strengths", result.get("strengths", [])),
        ("Suggestions", result.get("suggestions", [])),
        ("Skills", result.get("skills", [])),
    ]

    for heading, values in key_sections:
        story.append(Paragraph(heading, styles["Heading2"]))
        if values:
            story.append(ListFlowable([Paragraph(str(item)) for item in values], bulletType="bullet", bulletIndent=18))
        else:
            story.append(Paragraph("No information available."))
        story.append(Spacer(1, 12))

    doc.build(story)
    return output_path
