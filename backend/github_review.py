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
        print(f"Error fetching PR: {response.status_code} - {response.text}")
        return None
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

def review_code(diff_text):
    if not diff_text or not diff_text.strip():
        print("No diff content found.")
        return

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
        print("Could not parse AI response as JSON. Raw output:")
        print(raw)
        return

    issues = result.get("issues", [])
    score, grade = calculate_score(issues)

    bugs = [i for i in issues if i["category"] == "bug"]
    practices = [i for i in issues if i["category"] == "bad_practice"]
    security = [i for i in issues if i["category"] == "security"]

    print(f"\n{'='*45}")
    print(f"  SCORE: {score}/10   GRADE: {grade}")
    print(f"{'='*45}\n")

    print(f"🐛 Bugs & Logic Errors ({len(bugs)})")
    for b in bugs:
        print(f"   [{b['severity'].upper()}] {b['description']}")

    print(f"\n⚠️  Bad Practices ({len(practices)})")
    for p in practices:
        print(f"   [{p['severity'].upper()}] {p['description']}")

    print(f"\n🔒 Security Issues ({len(security)})")
    for s in security:
        print(f"   [{s['severity'].upper()}] {s['description']}")

    print(f"\n✅ Done Well ({len(result.get('positives', []))})")
    for pos in result.get("positives", []):
        print(f"   - {pos}")

    print(f"\n📝 Summary: {result.get('summary', 'N/A')}\n")

if __name__ == "__main__":
    owner = "Venkatesh496455"
    repo = "assignment-sentinel"
    pr_number = 1

    diff = get_pr_diff(owner, repo, pr_number)
    review_code(diff)