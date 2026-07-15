import os
import sys
from core import review_pr

def format_comment(result):
    if "error" in result:
        return f"⚠️ **Assignment Sentinel could not complete the review**\n\n{result['error']}"

    lines = [
        f"## 🛡️ Assignment Sentinel Review",
        f"**Score: {result['score']}/10 — Grade: {result['grade']}**",
        f"",
        f"{result['summary']}",
        f""
    ]

    def add_section(title, items):
        if items:
            lines.append(f"### {title} ({len(items)})")
            for item in items:
                lines.append(f"- **[{item['severity'].upper()}]** {item['description']}")
            lines.append("")

    add_section("🐛 Bugs & Logic Errors", result.get("bugs", []))
    add_section("⚠️ Bad Practices", result.get("bad_practices", []))
    add_section("🔒 Security Issues", result.get("security_issues", []))

    if result.get("positives"):
        lines.append("### ✅ Done Well")
        for p in result["positives"]:
            lines.append(f"- {p}")

    lines.append("\n---\n*Automated review by [Assignment Sentinel](https://github.com/Venkatesh496455/assignment-sentinel)*")

    return "\n".join(lines)

def post_comment(owner, repo, pr_number, body):
    import requests
    token = os.getenv("GITHUB_TOKEN")
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.post(url, headers=headers, json={"body": body})
    if response.status_code != 201:
        print(f"Failed to post comment: {response.status_code} - {response.text}")
        sys.exit(1)
    print("Comment posted successfully.")

if __name__ == "__main__":
    owner = os.getenv("REPO_OWNER")
    repo = os.getenv("REPO_NAME")
    pr_number = int(os.getenv("PR_NUMBER"))

    result = review_pr(owner, repo, pr_number)
    comment = format_comment(result)
    post_comment(owner, repo, pr_number, comment)
