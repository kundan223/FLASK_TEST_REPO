import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


def analyze_transaction(data):
    """
    Analyze a transaction using the Gemini API or fallback mock logic.
    Logs prompts and responses for debugging and transparency.
    """

    # 1️⃣ Enhanced prompt with reasoning structure
    prompt_text = f"""
You are a financial fraud detection assistant. 
Your job is to classify a transaction as either **Fraudulent** or **Not Fraudulent** based on common fraud patterns.

Analyze carefully using the transaction details below and follow these strict rules:
- Output ONLY one word: **"Fraudulent"** or **"Not Fraudulent"** (no explanations).
- Consider the following:
    • Transactions much higher than user's usual range may be suspicious.
    • If the location or device is unusual for this user, it could be fraud.
    • If the merchant is known for risky categories (e.g., gambling, crypto), it could be fraud.
    • Otherwise, assume it's a normal transaction.

Here are some examples to learn the pattern:
Example 1:
User: Rahul
Amount: 8000
Location: New York
Device: Unknown
→ Fraudulent

Example 2:
User: Ananya
Amount: 500
Location: Delhi
Device: iPhone 13
→ Not Fraudulent

Now, analyze the following transaction:

User: {data['user_name']}
Amount: {data['amount']}
Location: {data['location']}
Device: {data['device']}

Return only "Fraudulent" or "Not Fraudulent".
"""

    print("\n📤 ---- PROMPT SENT TO GEMINI ----")
    print(prompt_text.strip())
    print("-----------------------------------")

    # 2️⃣ Fallback logic if no API key
    if not GEMINI_API_KEY:
        print("(Mock mode) No Gemini API key found — using offline logic.")
        if float(data["amount"]) > 5000:
            result_text = "Fraudulent"
        else:
            result_text = "Not Fraudulent"

        _log_prompt(prompt_text, result_text)
        return result_text

    # 3️⃣ Prepare headers and body
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }

    body = {
        "contents": [
            {
                "parts": [{"text": prompt_text}],
                "role": "user"
            }
        ],
        "generationConfig": {
            "temperature": 0.0,  # deterministic output
            "maxOutputTokens": 10
        }
    }

    try:
        # 4️⃣ Send request
        response = requests.post(BASE_URL, headers=headers, json=body)
        response.raise_for_status()
        resp_json = response.json()

        print("\n📥 ---- RAW RESPONSE FROM GEMINI ----")
        print(json.dumps(resp_json, indent=2))
        print("-----------------------------------")

        # 5️⃣ Parse output safely
        result_text = None
        try:
            result_text = resp_json["candidates"][0]["content"]["parts"][0]["text"]
        except KeyError:
            try:
                result_text = resp_json["candidates"][0]["output_text"]
            except KeyError:
                result_text = json.dumps(resp_json, indent=2)

        result_text = result_text.strip().split()[0]  # only keep first word

        print(f"\n✅ Extracted Response: {result_text}\n")

        # 6️⃣ Log results
        _log_prompt(prompt_text, result_text)
        return result_text

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Gemini API request failed: {e}")
        result_text = "Not Fraudulent"
        _log_prompt(prompt_text, f"Error: {e}")
        return result_text


def _log_prompt(prompt_text: str, result_text: str):
    """Helper to log prompt and model output for debugging."""
    os.makedirs("prompt", exist_ok=True)
    log_path = "prompt/llm-chat-export.txt"

    with open(log_path, "a", encoding="utf-8") as f:
        f.write("📤 PROMPT SENT TO GEMINI:\n")
        f.write(prompt_text.strip() + "\n\n")
        f.write("📥 RESPONSE RECEIVED:\n")
        f.write(result_text.strip() + "\n")
        f.write("-" * 70 + "\n")
