from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
assistant = client.beta.assistants.create(
  name="Math Tutor",
  instructions="You are a personal math tutor. Write and run code to answer math questions.",
  tools=[{"type": "file_search"}],
  model="gpt-4o-mini",
)

print(f"--- assistant created: {assistant.id} ---")
def create_file(client, file_path):
    with open(file_path, "rb") as file_content:
      result = client.files.create(
          file=file_content,
          purpose="assistants"
      )
    return result.id

file_path = "../data/mvt.pdf"
file_id = create_file(client, file_path)
print(f"--- file created: {file_id} ---")

vector_store = client.vector_stores.create(
    name="knowledge_base"
)

print(f"--- vector store created: {vector_store.id} ---")
client.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=file_id
)

result = client.vector_stores.files.list(
    vector_store_id=vector_store.id
)
print(f"--- vector store files: {result} ---")

thread = client.beta.threads.create()
print(f"--- thread created: {thread.id} ---")

ids = {
    "assistant_id": assistant.id,
    "vector_store_id": vector_store.id,
    "file_id": file_id,
    "thread_id": thread.id
}
with open("ids.json", "w") as f:
    json.dump(ids, f)
print("--- IDs saved to ids.json ---")