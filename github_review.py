import os
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

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

def review_code(diff_text):
    if not diff_text or not diff_text.strip():
        print("No diff content found.")
        return

    prompt = f"""You are a strict but helpful code reviewer for a student developer.
Review the following pull request diff. Point out:
1. Bugs or logic errors
2. Bad practices (naming, structure, missing error handling)
3. Security issues (hardcoded secrets, unsafe input handling)
4. One thing done well

Be concise and specific, referencing line changes. Diff:

{diff_text}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    print("\n=== AI PR REVIEW ===\n")
    print(response.text)

if __name__ == "__main__":
    owner = "Venkatesh496455"
    repo = "assignment-sentinel"
    pr_number = 1

    diff = get_pr_diff(owner, repo, pr_number)
    review_code(diff)