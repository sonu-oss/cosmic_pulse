import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=r"C:\Users\C M Raju\Desktop\GDGproj\keys.env", override=True)

import google.generativeai as genai
from groq import Groq
from knowledge_engine import query_knowledge

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise EnvironmentError("GOOGLE_API_KEY not found in keys.env")

os.environ["GEMINI_API_KEY"] = api_key
genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=(
        "You are a Scientific Advisor. Use a clear, precise, evidence-focused tone. "
        "Answer questions based ONLY on the provided context. If the answer isn't "
        "present in the context, say: 'I don't have enough context in the knowledge base to answer that.' "
        "Do not add outside facts or hallucinate information."
    )
)

def ask_cosmic_agent(user_question):
    context = query_knowledge(user_question)
    if not context or not context.strip():
        return "I could not find relevant context in the knowledge base."
    prompt = f"Context:\n{context}\n\nUser Question:\n{user_question}"
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.0)
        )
        return response.text.strip()
    except Exception as exc:
        return f"Failed to generate response: {exc}"

def ask_free_chatbot(chat_history):
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        return "Error: GROQ_API_KEY not found in keys.env"
    
    client = Groq(api_key=groq_key)
    messages = [{"role": "system", "content": (
        "You are CosmicPulse, an enthusiastic AI space expert. "
        "Answer any question about space, astronomy, missions, physics, or the universe. "
        "Be engaging, accurate, and inspiring."
    )}]
    for msg in chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        return f"Error: {exc}"