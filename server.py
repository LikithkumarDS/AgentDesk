import os
import time
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from google import genai
from google.genai import errors, types
from pydantic import BaseModel

from models import ContentPiece, ReviewReport, Topic, TopicReport
from reviewer_agent import ReviewerAgent
from writer_agent import WriterAgent

load_dotenv()

app = FastAPI(title="AI Agentic Content Studio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_ID = "gemini-3.8-flash"
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

writer = WriterAgent()
writer.model_id = MODEL_ID
reviewer = ReviewerAgent()
reviewer.model_id = MODEL_ID

app.mount("/static", StaticFiles(directory="static"), name="static")


def run_with_retry(fn, retries: int = 4, delay: int = 3):
    for attempt in range(retries):
        try:
            return fn()
        except errors.APIError as e:
            if any(code in str(e) for code in ("503", "500", "429")) and attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
                continue
            raise


@app.get("/")
def serve_dashboard():
    return FileResponse("static/index.html")


class ResearchRequest(BaseModel):
    niche: str


class RefineRequest(BaseModel):
    article: ContentPiece
    review: ReviewReport


@app.post("/api/research", response_model=TopicReport)
def api_research(req: ResearchRequest):
    if not req.niche.strip():
        raise HTTPException(status_code=400, detail="Niche cannot be empty.")
    try:
        response = run_with_retry(
            lambda: client.models.generate_content(
                model=MODEL_ID,
                contents=f"Find 3 trending topics for {req.niche}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=TopicReport,
                    system_instruction="You are a trend analyst finding real, current, and emerging topics.",
                ),
            )
        )
        return response.parsed
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/write", response_model=ContentPiece)
def api_write(topic: Topic):
    try:
        return run_with_retry(lambda: writer.write_article(topic))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/review", response_model=ReviewReport)
def api_review(article: ContentPiece):
    try:
        return run_with_retry(lambda: reviewer.review_article(article))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/refine", response_model=ContentPiece)
def api_refine(req: RefineRequest):
    try:
        return run_with_retry(lambda: writer.refine_article(req.article, req.review))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)