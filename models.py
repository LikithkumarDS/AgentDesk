from pydantic import BaseModel, Field
from typing import List

class Topic(BaseModel):
    title: str
    description: str
    why_now: str

class TopicReport(BaseModel):
    suggested_topics: List[Topic]

class ContentPiece(BaseModel):
    title: str
    hook: str
    body: str
    call_to_action: str

class ReviewReport(BaseModel):
    score: int = Field(description="Score from 1 to 10")
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: str
    fact_check_notes: str