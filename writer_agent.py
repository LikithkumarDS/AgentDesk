import os
import re
from google import genai
from google.genai import types
from models import Topic, ContentPiece, ReviewReport

class WriterAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-3.5-flash-lite"

    def write_article(self, topic: Topic) -> ContentPiece:
        print(f"✍️ Writer Agent is crafting: {topic.title}...")
        chat = self.client.chats.create(
            model=self.model_id,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ContentPiece,
                system_instruction="You are a professional journalist."
            )
        )
        response = chat.send_message(f"Write an article about {topic.title}. Context: {topic.description}")
        return response.parsed

    def refine_article(self, original_article: ContentPiece, review: ReviewReport) -> ContentPiece:
        print(f"🔄 Writer Agent is refining based on feedback...")
        chat = self.client.chats.create(
            model=self.model_id,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ContentPiece,
                system_instruction="You are an editor. Improve the article based on feedback."
            )
        )
        prompt = f"Original: {original_article.body}\n\nFeedback: {review.improvement_suggestions}"
        response = chat.send_message(prompt)
        return response.parsed

    def save_to_file(self, article: ContentPiece):
        filename = re.sub(r'[^\w\s-]', '', article.title).strip().replace(' ', '_') + ".txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"TITLE: {article.title}\n\n{article.body}")
        print(f"💾 Saved: {filename}")

        import os
import re
from google import genai
from google.genai import types
from models import Topic, ContentPiece, ReviewReport

class WriterAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-3.5-flash-lite"

    def write_article(self, topic: Topic) -> ContentPiece:
        print(f"✍️ Writer Agent is crafting a short article: {topic.title}...")
        chat = self.client.chats.create(
            model=self.model_id,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ContentPiece,
                # CHANGED: Added "concise" and "short form" instructions
                system_instruction="You are a short-form content creator. Write punchy, concise, and high-impact articles under 200 words."
            )
        )
        # CHANGED: Explicitly asked for a "short article"
        prompt = f"Write a short, 3-paragraph article about {topic.title}. Keep it under 200 words total."
        response = chat.send_message(prompt)
        return response.parsed

    def refine_article(self, original_article: ContentPiece, review: ReviewReport) -> ContentPiece:
        print(f"🔄 Writer Agent is refining (keeping it short)...")
        chat = self.client.chats.create(
            model=self.model_id,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ContentPiece,
                system_instruction="You are an editor specializing in brevity. Improve the content without increasing the length."
            )
        )
        prompt = f"Original: {original_article.body}\n\nFeedback: {review.improvement_suggestions}\n\nTask: Fix the issues but keep the article short and punchy."
        response = chat.send_message(prompt)
        return response.parsed

    def save_to_file(self, article: ContentPiece):
        filename = re.sub(r'[^\w\s-]', '', article.title).strip().replace(' ', '_') + "_short.txt"
        with open(filename, "w", encoding="utf-8") as f:
              f.write(f"TITLE: {article.title}\n\n{article.body}")
        print(f"💾 Short Article Saved: {filename}")

        import os
import re
import subprocess  # Added to allow opening the file automatically
from google import genai
from google.genai import types
from models import Topic, ContentPiece, ReviewReport

class WriterAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-3.5-flash-lite"

    def write_article(self, topic: Topic) -> ContentPiece:
        print(f"✍️ Writer Agent is crafting: {topic.title}...")
        chat = self.client.chats.create(
            model=self.model_id,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ContentPiece,
                system_instruction="You are a professional content creator. Write short, punchy articles."
            )
        )
        response = chat.send_message(f"Write a short, 3-paragraph article about {topic.title}")
        return response.parsed

    def refine_article(self, original_article: ContentPiece, review: ReviewReport) -> ContentPiece:
        print(f"🔄 Writer Agent is refining based on feedback...")
        chat = self.client.chats.create(
            model=self.model_id,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ContentPiece,
                system_instruction="You are an editor. Improve the content based on feedback."
            )
        )
        prompt = f"Original: {original_article.body}\n\nFeedback: {review.improvement_suggestions}"
        response = chat.send_message(prompt)
        return response.parsed

    def save_to_file(self, article: ContentPiece):
        """Saves the article and opens it automatically."""
        # Create a clean filename
        clean_title = re.sub(r'[^\w\s-]', '', article.title).strip().replace(' ', '_')
        filename = f"{clean_title}.txt"
        
        # 1. Write the file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"TITLE: {article.title}\n")
            print("-" * 20)
            f.write(f"\n{article.body}\n")
            f.write(f"\n--- GENERATED BY AI AGENT TEAM ---")
        
        print(f"💾 File saved: {filename}")

        # 2. AUTO-OPEN THE FILE (Windows specific)
        try:
            os.startfile(filename) # This will pop the file open in Notepad
        except Exception:
            # If for some reason startfile fails (non-windows), try subprocess
            subprocess.call(['open', filename])