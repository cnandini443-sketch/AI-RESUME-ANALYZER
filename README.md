
# AI Resume Analyzer & Career Assistant

A Flask-based portfolio-ready resume analysis app that helps users evaluate and improve their resume for job applications.

## Features

- Upload PDF or DOCX resumes
- Extract and clean text from uploaded files
- Detect technical and soft skills
- Score resume quality and ATS compatibility
- Compare resumes against a job description
- Recommend role fits and skill gaps
- Suggest resume improvements and stronger bullet points
- Generate interview practice questions
- Save analysis history in SQLite
- Download a PDF summary report

## Tech Stack

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Vanilla JavaScript
- PyPDF2
- python-docx
- ReportLab

## Run locally

### 1. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the application

```bash
python app.py
```

### 4. Open the app

- Home page: http://127.0.0.1:5000/
- Dashboard: http://127.0.0.1:5000/dashboard
- History: http://127.0.0.1:5000/history

## Notes

This project uses a lightweight rule-based analyzer for beginner-friendly performance and transparency. It can be extended later with advanced AI models or external APIs without changing the core workflow.
