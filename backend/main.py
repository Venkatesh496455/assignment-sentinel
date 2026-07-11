from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core import review_pr

app = FastAPI(title="Assignment Sentinel API")

# Allow the React frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for local dev; we'll restrict this later
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Assignment Sentinel API is running"}

@app.get("/review")
def review(owner: str, repo: str, pr_number: int):
    try:
        result = review_pr(owner, repo, pr_number)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))