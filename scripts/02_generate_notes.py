import json
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class Note(BaseModel):
    id: int = Field(..., ge=1, le=10)
    heading: str
    summary: str = Field(..., max_length=150)
    page_ref: int | None = None

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("ids.json", "r") as f:
    ids = json.load(f)

assistant_id = ids["assistant_id"]
vector_store_id = ids["vector_store_id"]
thread_id = ids["thread_id"]

client.beta.assistants.update(
    assistant_id=assistant_id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
)
print("--- client loaded ---")

system = (
    "You are a study summarizer. Read the uploaded calculus PDF. "
    "Return exactly 10 revision notes in **this exact JSON format**:\n\n"
    "[\n"
    "  {\n"
    "    \"id\": 1,\n"
    "    \"heading\": \"Mean Value Theorem\",\n"
    "    \"summary\": \"Explains the MVT: if f is continuous and differentiable, there exists a point where f’ equals avg rate.\",\n"
    "    \"page_ref\": 23\n"
    "  },\n"
    "  ... (9 more)\n"
    "]\n\n"
    "Each note must be short (summary ≤ 150 characters) and helpful for revision. "
    "Respond with **only JSON** — no commentary, no markdown, no explanation."
)

client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=system
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id,
    assistant_id=assistant_id
)

# Get the latest messages
messages = client.beta.threads.messages.list(thread_id=thread_id)
latest = messages.data[0].content[0].text.value

# Clean code block markers (if present)
if latest.startswith("```json"):
    latest = latest.strip("```json").strip("```").strip()
elif latest.startswith("```"):
    latest = latest.strip("```").strip()

# Parse and validate
try:
    data = json.loads(latest)
    notes = [Note(**item) for item in data]
    print(f"\n--- generated {len(notes)} notes ---\n")
    for note in notes:
        print(f"{note.id}. {note.heading} — {note.summary} (p.{note.page_ref})")
    
    with open("exam.json", "w") as f:
        json.dump(data, f, indent=2)
    print("--- saved to exam.json ---")

except Exception as e:
    print("error parsing or validating the notes:")
    print(e)
    print("--- raw content ---")
    print(latest)