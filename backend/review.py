import os
import subprocess
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_git_diff():
    result = subprocess.run(
        ["git", "diff", "--cached"],
        capture_output=True, text=True
    )
    return result.stdout

def review_code(diff_text):
    if not diff_text.strip():
        print("No staged changes found. Stage some changes with 'git add' first.")
        return

    prompt = f"""You are a strict but helpful code reviewer for a student developer.
Review the following git diff. Point out:
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
    print("\n=== AI CODE REVIEW ===\n")
    print(response.text)

if __name__ == "__main__":
    diff = get_git_diff()
    review_code(diff)