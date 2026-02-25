import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Test text
text = """
NASA's James Webb Space Telescope has captured the deepest
infrared image of the universe ever taken, showing thousands
of galaxies that existed less than a billion years after the
Big Bang. The image represents 12.5 hours of observations and
covers a patch of sky smaller than a grain of sand held at
arm's length. Scientists say this is just the beginning of
what Webb will reveal about the early universe.
"""

SYSTEM_PROMPT = """You are a summarization engine. Given text, return ONLY a valid JSON object with exactly this structure:
{
  "summary": "2-3 sentence summary of the text",
  "bullets": ["key point 1", "key point 2", "key point 3"],
  "title": "a suggested title for the text"
}
No explanation. No markdown. No code blocks. Only the raw JSON object."""

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Summarize this text:\n\n{text}"}
    ],
    temperature=0.3,  # low temperature = more consistent output
    max_tokens=512
)

raw = response.choices[0].message.content
print("Raw output:")
print(raw)

# Try parsing as JSON
import json
try:
    result = json.loads(raw)
    print("\n--- Parsed ---")
    print(f"Title:   {result['title']}")
    print(f"Summary: {result['summary']}")
    print(f"Bullets:")
    for b in result['bullets']:
        print(f"  - {b}")
except json.JSONDecodeError:
    print("\nJSON parsing failed — need to fix the prompt")
