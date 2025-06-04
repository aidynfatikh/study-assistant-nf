import json
import os
from openai import OpenAI
from dotenv import load_dotenv
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("ids.json", "r") as f:
    ids = json.load(f)

assistant_id = ids["assistant_id"]
vector_store_id = ids["vector_store_id"]
file_id = ids["file_id"]

client.beta.assistants.update(
    assistant_id=assistant_id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
)

thread = client.beta.threads.create()
print(f"--- thread created: {thread.id} ---")

question = "what is the pdf about?"
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=question
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant_id
)
messages = client.beta.threads.messages.list(thread_id=thread.id)

print(f"\n--- question: {question} ---")
print("--- assistant response ---\n")
for message in messages.data:
    if message.role == "assistant":
        for content in message.content:
            print(content.text.value)

        if message.metadata and "citations" in message.metadata:
            print("\n--- citations ---")
            print(message.metadata["citations"])
