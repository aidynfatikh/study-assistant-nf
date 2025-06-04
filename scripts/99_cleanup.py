from openai import OpenAI
from dotenv import load_dotenv
import os
import json

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
with open("ids.json", "r") as f:
    ids = json.load(f)

assistant_id = ids["assistant_id"]
vector_store_id = ids["vector_store_id"]
file_id = ids["file_id"]
thread_id = ids["thread_id"]

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print(f"--- deleting file: {file_id} ---")
client.files.delete(file_id)
print(f"--- deleting vector store: {vector_store_id} ---")
client.vector_stores.delete(vector_store_id)
print(f"--- deleting thread: {thread_id} ---")
client.beta.threads.delete(thread_id)
print(f"--- deleting assistant: {assistant_id} ---")
client.beta.assistants.delete(assistant_id)
print("--- cleanup complete ---")