import os
import time
from typing import List
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

# 1. Define the Schema
class Topic(BaseModel):
    title: str
    description: str
    why_now: str

class TopicReport(BaseModel):
    suggested_topics: List[Topic]

def run_generator():
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    # In 2026, 3.5-flash-lite is the best for high-speed structured tasks
    MODEL_ID = "gemini-3.5-flash-lite" 

    niche = input("\nEnter your niche (e.g., Road Trips): ")
    print(f"🔎 Agent is searching the web for 2026 trends in '{niche}'...")

    try:
        # Create a Chat session - this follows the "Recommended" way to use tools
        chat = client.chats.create(
            model=MODEL_ID,
            config=types.GenerateContentConfig(
            
                response_mime_type="application/json",
                response_schema=TopicReport,
                system_instruction="You are a trend scout. Find 3 fresh, specific road trip trends for late 2026."
            )
        )

        response = chat.send_message(f"What are 3 trending road trip topics for {niche}?")
        
        # Access the parsed data
        report: TopicReport = response.parsed
        
        print(f"\n✅ SUCCESS! TRENDING TOPICS FOR {niche.upper()}:")
        for t in report.suggested_topics:
            print(f"\n📌 {t.title}")
            print(f"   - {t.description}")
            print(f"   - Why it's hot: {t.why_now}")

    except Exception as e:
        if "429" in str(e):
            print("\n❌ Rate Limit Hit! The Free Tier only allows a few searches per minute.")
            print("Please wait 60 seconds and try again.")
        else:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    print("--- 2026 Topic Agent Ready ---")
    run_generator()