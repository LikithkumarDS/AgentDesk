import os
from google import genai
from google.genai import types
from models import ContentPiece, ReviewReport

class ReviewerAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-3.5-flash-lite"

    def review_article(self, article: ContentPiece) -> ReviewReport:
        print(f"🧐 Reviewer Agent is analyzing quality...")
        chat = self.client.chats.create(
            model=self.model_id,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ReviewReport,
                system_instruction="You are a harsh but fair Editorial Director."
            )
        )
        prompt = f"Review this: {article.title}\n{article.body}"
        response = chat.send_message(prompt)
        return response.parsed