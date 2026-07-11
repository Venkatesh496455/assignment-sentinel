import os
import json
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

SEVERITY_WEIGHTS = {
    "critical": 3.0,
    "major": 1.5,
    "minor": 0.5
}

def get_pr_diff(owner, repo, pr_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"GitHub API error {response.status_code}: {response.text}")
    return response.text

def calculate_score(issues):
    score = 10.0
    for issue in issues:
        weight = SEVERITY_WEIGHTS.get(issue.get("severity", "minor"), 0.5)
        score -= weight
    score = max(0, round(score, 1))

    if score >= 9:
        grade = "A"
    elif score >= 7:
        grade = "B"
    elif score >= 5:
        grade = "C"
    elif score >= 3:
        grade = "D"
    else:
        grade = "F"

    return score, grade

def review_pr(owner, repo, pr_number):
    diff_text = get_pr_diff(owner, repo, pr_number)

    if not diff_text or not diff_text.strip():
        return {"error": "No diff content found."}

    prompt = f"""You are a strict, professional code reviewer. Analyze this pull request diff.

For EVERY issue you find, classify its severity as exactly one of: "critical", "major", or "minor".
- critical: security vulnerabilities, data loss risks, crashes, broken functionality
- major: bad practices that will cause real problems (no error handling, poor structure, logic errors)
- minor: style issues, naming, missing comments, trivial formatting

Respond ONLY with valid JSON (no markdown, no backticks, no extra text) in exactly this structure:

{{
  "issues": [
    {{"category": "bug", "severity": "critical", "description": "..."}},
    {{"category": "bad_practice", "severity": "minor", "description": "..."}}
  ],
  "positives": ["thing done well"],
  "summary": "one to two sentence overall verdict"
}}

category must be one of: "bug", "bad_practice", "security".
If there are no issues at all, use an empty list for "issues". Diff to review:

{diff_text}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    raw = response.text.strip().replace("```json", "").replace("```", "")

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        return {"error": "Could not parse AI response.", "raw": raw}

    issues = result.get("issues", [])
    score, grade = calculate_score(issues)

    return {
        "score": score,
        "grade": grade,
        "bugs": [i for i in issues if i["category"] == "bug"],
        "bad_practices": [i for i in issues if i["category"] == "bad_practice"],
        "security_issues": [i for i in issues if i["category"] == "security"],
        "positives": result.get("positives", []),
        "summary": result.get("summary", "")
    }
