import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "resume_analyzer.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                job_description TEXT,
                score REAL,
                ats_score REAL,
                match_score REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                summary TEXT,
                details TEXT
            )
            """
        )


def save_analysis(filename, job_description, result):
    payload = {
        "filename": filename,
        "job_description": job_description,
        "result": result,
    }
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO analyses (filename, job_description, score, ats_score, match_score, summary, details)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                filename,
                job_description,
                float(result.get("score", 0) or 0),
                float(result.get("ats_score", 0) or 0),
                float(result.get("job_match", {}).get("match_score", 0) or 0),
                (result.get("job_match", {}).get("summary") or "Resume analyzed successfully."),
                json.dumps(payload, ensure_ascii=False),
            ),
        )
        return cursor.lastrowid


def get_history():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, filename, job_description, score, ats_score, match_score, created_at, summary
            FROM analyses
            ORDER BY created_at DESC
            LIMIT 25
            """
        ).fetchall()

    history = []
    for row in rows:
        history.append({
            "id": row["id"],
            "filename": row["filename"],
            "job_description": row["job_description"],
            "score": row["score"],
            "ats_score": row["ats_score"],
            "match_score": row["match_score"],
            "created_at": row["created_at"],
            "summary": row["summary"],
        })
    return history


def get_analysis_by_id(analysis_id):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, filename, job_description, score, ats_score, match_score, created_at, summary, details
            FROM analyses
            WHERE id = ?
            """,
            (analysis_id,),
        ).fetchone()

    if row is None:
        return None

    details = json.loads(row["details"]) if row["details"] else {}
    return {
        "id": row["id"],
        "filename": row["filename"],
        "job_description": row["job_description"],
        "score": row["score"],
        "ats_score": row["ats_score"],
        "match_score": row["match_score"],
        "created_at": row["created_at"],
        "summary": row["summary"],
        "details": details.get("result", details),
    }
