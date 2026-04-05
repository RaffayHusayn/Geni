from openai import OpenAI
from dotenv import load_dotenv
from ingestionPrompts import PROMPTS
import time
import json

load_dotenv()
MAX_RETRIES = 2
RETRY_DELAY = 1

def llmParser(text: str)->dict:
    client = OpenAI()
    prompt = PROMPTS["parser"].format(text=text[:6000])

    for attempt in range(1, MAX_RETRIES+1):
        try:
            response = client.chat.completions.create(
                model="gpt-5-mini",
                messages=[
                    {"role":"system", "content": "You are a precise data extraction assistant. Output strictly in JSON format."},
                    {"role":"user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content
            if content is None:
                raise ValueError("Content returned is None")
            content = content.strip()
            parsed = json.loads(content)
            if not isinstance(parsed, dict):
                raise ValueError(f"Expected JSON object, got {type(parsed).__name__}")
            return parsed
        except json.JSONDecodeError as e:
            print(f"[Attempt {attempt}] JSON decode error: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                raise ValueError("Failed to parse JSON after multiple attempts.") from e
        except Exception as e:
            print(f"[Attempt {attempt}] Unexpected error: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                raise
    raise RuntimeError("All retries return no content")