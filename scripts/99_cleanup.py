from openai import OpenAI
from dotenv import load_dotenv
import os
import json

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

if os.path.exists("ids.json"):
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    with open("ids.json", "r") as f:
        ids = json.load(f)

    assistant_id = ids["assistant_id"]
    vector_store_id = ids["vector_store_id"]
    file_id = ids["file_id"]
    thread_id = ids["thread_id"]

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        print(f"--- deleting file: {file_id} ---")
        client.files.delete(file_id)
    except Exception as e:
        print("--- error deleting file (probably already deleted) ---")

    try:
        print(f"--- deleting vector store: {vector_store_id} ---")
        client.vector_stores.delete(vector_store_id)
    except Exception as e:
        print("--- error deleting vector store (probably already deleted) ---")

    try:
        print(f"--- deleting thread: {thread_id} ---")
        client.beta.threads.delete(thread_id)
    except Exception as e:
        print("--- error deleting thread (probably already deleted) ---")

    try:
        print(f"--- deleting assistant: {assistant_id} ---")
        client.beta.assistants.delete(assistant_id)
    except Exception as e:
        print("--- error deleting assistant (probably already deleted) ---")

    # Remove ids.json file
    os.remove("ids.json")
    print("--- ids.json removed ---")
    print("--- cleanup complete ---")
else:
    print("--- ids.json not found ---")
    print("--- exiting cleanup ---")