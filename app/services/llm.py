import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a summarization engine. Given text, return ONLY a valid JSON object with exactly this structure:
{
  "summary": "2-3 sentence summary of the text",
  "bullets": ["key point 1", "key point 2", "key point 3"],
  "title": "a suggested title for the text"
}
No explanation. No markdown. No code blocks. Only the raw JSON object."""

def get_summary(text: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Summarize this text:\n\n{text}"}
        ],
        temperature=0.3,
        max_tokens=512
    )
    raw = response.choices[0].message.content
    return json.loads(raw)
