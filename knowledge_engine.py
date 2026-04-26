import os
import chromadb
from dotenv import load_dotenv
load_dotenv(dotenv_path=r"C:\Users\C M Raju\Desktop\GDGproj\keys.env", override=True)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise EnvironmentError("❌ GOOGLE_API_KEY not found in keys.env!")

os.environ["GEMINI_API_KEY"] = api_key

from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction

google_ef = GoogleGenerativeAiEmbeddingFunction(api_key=api_key)
client = chromadb.PersistentClient(path="./chroma_db")

def index_mission_data(file_path):
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found!")
        return
    collection = client.get_or_create_collection(
        name="space_missions",
        embedding_function=google_ef
    )
    with open(file_path, "r", encoding="utf-8") as f:
        content = [p.strip() for p in f.read().split("\n\n") if p.strip()]
    if not content:
        print("⚠️ Warning: mission_info.txt is empty.")
        return
    ids = [f"id_{i}" for i in range(len(content))]
    collection.add(documents=content, ids=ids)
    print(f"✅ SUCCESS: Indexed {len(content)} space mission facts.")

def query_knowledge(user_query):
    collection = client.get_or_create_collection(
        name="space_missions",
        embedding_function=google_ef
    )
    results = collection.query(query_texts=[user_query], n_results=2)
    if results and results['documents'] and len(results['documents']) > 0:
        return " ".join(results['documents'][0])
    return ""

if __name__ == "__main__":
    print("🧹 Cleaning up old database...")
    try:
        client.delete_collection(name="space_missions")
    except:
        pass
    index_mission_data("mission_info.txt")