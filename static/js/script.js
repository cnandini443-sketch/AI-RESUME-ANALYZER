
function renderTagList(elementId, values, missingClass = false) {
  const el = document.getElementById(elementId);
  if (!el) return;

  if (!values || values.length === 0) {
    el.innerHTML = '<span class="muted-empty">No matching items found.</span>';
    return;
  }

  el.innerHTML = values
    .map((value) => `<span class="chip ${missingClass ? "missing" : ""}">${value}</span>`)
    .join("");
}

function renderSections(sections) {
  const el = document.getElementById("sections");
  if (!el) return;
  const rows = Object.entries(sections || {}).map(([key, present]) => `
    <div class="check-row">
      <strong>${key.charAt(0).toUpperCase() + key.slice(1)}</strong>
      <span>${present ? "✓" : "—"}</span>
    </div>
  `);
  el.innerHTML = rows.join("");
}

function renderRoleList(roles) {
  const el = document.getElementById("roles");
  if (!el) return;
  if (!roles || roles.length === 0) {
    el.innerHTML = '<p>No role recommendations yet.</p>';
    return;
  }

  el.innerHTML = roles
    .map(
      (role) => `
        <div class="role-item">
          <div class="role-header">
            <span>${role.role}</span>
            <span>${role.match}%</span>
          </div>
          <div class="progress-bar"><div class="progress-fill" style="width:${role.match}%"></div></div>
        </div>
      `
    )
    .join("");
}

function renderList(elementId, values) {
  const el = document.getElementById(elementId);
  if (!el) return;
  if (!values || values.length === 0) {
    el.innerHTML = '<li>No items to display.</li>';
    return;
  }
  el.innerHTML = values.map((item) => `<li>${item}</li>`).join("");
}

function renderOrderedList(elementId, values) {
  const el = document.getElementById(elementId);
  if (!el) return;
  if (!values || values.length === 0) {
    el.innerHTML = '<li>No interview questions generated.</li>';
    return;
  }
  el.innerHTML = values.map((item) => `<li>${item}</li>`).join("");
}

function renderResults(data) {
  document.getElementById("score").textContent = data.score || 0;
  document.getElementById("scoreBadge").textContent = `${data.score || 0}/100`;
  document.getElementById("atsScore").textContent = data.ats_score || 0;
  document.getElementById("jobMatchValue").textContent = `${data.job_match?.match_score || 0}%`;
  document.getElementById("jobMatchSummary").textContent = data.job_match?.summary || "Awaiting JD";
  document.getElementById("wordCount").textContent = data.word_count || 0;
  document.getElementById("topRole").textContent = data.top_role || "N/A";

  renderTagList("skills", data.skills || []);
  renderTagList("missingSkills", data.missing_skills || [], true);
  renderTagList("matchedKeywords", data.job_match?.matched_keywords || []);
  renderTagList("missingKeywords", data.job_match?.missing_keywords || [], true);
  renderSections(data.sections || {});
  renderRoleList(data.roles || []);
  renderList("strengths", data.strengths || []);
  renderList("suggestions", data.suggestions || []);
  renderOrderedList("interviewQuestions", data.interview_questions || []);

  const reportLink = document.getElementById("downloadReport");
  if (data.analysis_id) {
    reportLink.href = `/download-report/${data.analysis_id}`;
    reportLink.style.display = "inline-flex";
  }

  const resultsBlock = document.getElementById("results");
  if (resultsBlock) resultsBlock.classList.remove("hidden");
  resultsBlock?.scrollIntoView({ behavior: "smooth", block: "start" });
}

function loadHistory() {
  fetch("/api/history")
    .then((res) => res.json())
    .then((payload) => {
      const list = document.getElementById("historyList");
      if (!list) return;
      if (!payload.history || payload.history.length === 0) {
        list.innerHTML = '<div class="history-item"><strong>No saved analyses yet.</strong><p class="history-meta">Generate a report from the dashboard to start building your history.</p></div>';
        return;
      }

      list.innerHTML = payload.history
        .map(
          (item) => `
            <div class="history-item">
              <strong>${item.filename}</strong>
              <p>${item.summary || "Resume analyzed successfully."}</p>
              <div class="history-meta">
                <span>Score: ${item.score}</span>
                <span>ATS: ${item.ats_score}</span>
                <span>Match: ${item.match_score}%</span>
                <span>${new Date(item.created_at).toLocaleString()}</span>
                <a href="/download-report/${item.id}">Download PDF</a>
              </div>
            </div>
          `
        )
        .join("");
    })
    .catch(() => {
      document.getElementById("historyList").innerHTML = '<div class="history-item"><strong>Unable to load history.</strong></div>';
    });
}

function setupDashboard() {
  const form = document.getElementById("resumeForm");
  const input = document.getElementById("resume");
  const fileName = document.getElementById("fileName");
  const statusText = document.getElementById("status");
  const button = document.getElementById("analyzeBtn");

  if (!form || !input) return;

  input.addEventListener("change", () => {
    fileName.textContent = input.files[0] ? input.files[0].name : "Choose PDF or DOCX file";
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const file = input.files[0];
    if (!file) {
      statusText.textContent = "Please select a resume file before analyzing.";
      return;
    }

    const formData = new FormData(form);
    statusText.textContent = "Analyzing your resume...";
    button.disabled = true;

    try {
      const response = await fetch("/analyze", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Analysis failed.");
      }
      renderResults(data);
      statusText.textContent = "Resume analyzed successfully.";
    } catch (error) {
      statusText.textContent = error.message;
    } finally {
      button.disabled = false;
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  setupDashboard();
  if (document.getElementById("historyList")) {
    loadHistory();
  }
});
