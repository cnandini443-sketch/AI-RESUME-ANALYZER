
import json
import uuid
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request, send_file
from werkzeug.utils import secure_filename

from database.db import get_analysis_by_id, get_history, init_db, save_analysis
from services.analyzer import analyze_resume
from services.report_generator import generate_report_pdf
from services.resume_parser import extract_text

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
REPORTS_FOLDER = BASE_DIR / "reports"
UPLOAD_FOLDER.mkdir(exist_ok=True)
REPORTS_FOLDER.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "docx"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/history")
def history_page():
    return render_template("history.html")


@app.route("/api/history")
def history_api():
    return jsonify({"history": get_history()})


@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return jsonify({"error": "Please upload a resume."}), 400

    file = request.files["resume"]
    if not file.filename:
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF and DOCX files are supported."}), 400

    temp_name = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    path = UPLOAD_FOLDER / temp_name
    file.save(path)

    try:
        text = extract_text(path)
        if len(text.strip()) < 50:
            return jsonify({"error": "Could not extract enough text from this resume."}), 400

        job_description = request.form.get("job_description", "") or ""
        result = analyze_resume(text, job_description)
        analysis_id = save_analysis(file.filename, job_description, result)
        result["analysis_id"] = analysis_id
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": f"Could not analyze the resume: {exc}"}), 500
    finally:
        if path.exists():
            path.unlink()


@app.route("/download-report/<int:analysis_id>")
def download_report(analysis_id):
    analysis = get_analysis_by_id(analysis_id)
    if not analysis:
        abort(404)

    pdf_path = generate_report_pdf(analysis)
    return send_file(pdf_path, as_attachment=True, download_name=f"resume_report_{analysis_id}.pdf")


init_db()


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
