import os
import time
from google import genai
from google.genai import errors

# 1. Setup Client
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Using the 'Lite' model which usually has much better availability
MODEL_ID = "gemini-3.5-flash-lite" 

def start_agent():
    print(f"🤖 Agent connecting to {MODEL_ID}...")
    
    max_retries = 3
    for i in range(max_retries):
        try:
            # We use the Chat session for agentic history
            chat = client.chats.create(model=MODEL_ID)
            response = chat.send_message("System check: Agent online. Respond with 'Ready'.")
            
            print(f"\nAgent Response: {response.text}")
            print("✅ Connection Stable.")
            return
            
        except errors.APIError as e:
            # This catches both 503 (Server) and 429 (Rate Limit) errors
            if "503" in str(e) or "500" in str(e):
                print(f"⚠️ Server busy (Attempt {i+1}/{max_retries}). Waiting 10s...")
                time.sleep(10)
            else:
                print(f"❌ API Error: {e}")
                break
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            break

if __name__ == "__main__":
    start_agent()