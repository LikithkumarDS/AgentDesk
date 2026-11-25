import os
from google import genai
from google.genai import types
from models import Topic, TopicReport
from writer_agent import WriterAgent
from reviewer_agent import ReviewerAgent

# Initialize Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def researcher_agent(niche: str):
    print(f"\n🔎 Researcher Agent: Finding 2026 trends for '{niche}'...")
    try:
        # Note: We temporarily removed tools=... to avoid 429 errors
        chat = client.chats.create(
            model="gemini-3.5-flash-lite",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=TopicReport,
                system_instruction="You are a trend analyst finding real 2026 topics."
            )
        )
        response = chat.send_message(f"Find 3 trending topics for {niche}")
        return response.parsed
    except Exception as e:
        print(f"❌ Research Error: {e}")
        return None

def run_team():
    print("\n" + "="*50)
    print("🚀 2026 AI AGENTIC CONTENT STUDIO")
    print("="*50)
    
    niche = input("\nEnter your niche: ")
    report = researcher_agent(niche)
    
    if not report: return

    print("\n--- 🔎 TOPICS FOUND ---")
    for i, t in enumerate(report.suggested_topics, 1):
        print(f"{i}. {t.title}")

    try:
        choice = int(input("\nSelect a topic (1-3): "))
        selected_topic = report.suggested_topics[choice - 1]
    except:
        return

    # Initialize Agents
    writer = WriterAgent()
    reviewer = ReviewerAgent()

    # Step 1: Write
    article = writer.write_article(selected_topic)

    # Step 2: Review
    review = reviewer.review_article(article)
    print(f"\n⭐ REVIEW SCORE: {review.score}/10")
    print(f"💡 SUGGESTION: {review.improvement_suggestions}")

    # Step 3: Refine (If score is between 5 and 9)
    if 5 <= review.score < 9:
        article = writer.refine_article(article, review)
        print("✨ Article Refined based on Editor's feedback!")

    # Step 4: Save
    if review.score >= 5:
        writer.save_to_file(article)
        print(f"\n✅ SUCCESS: Final version saved.")
    else:
        print("\n❌ Quality too low.")

if __name__ == "__main__":
    run_team()