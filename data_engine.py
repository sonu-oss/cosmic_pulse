import requests
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=r"C:\Users\C M Raju\Desktop\GDGproj\keys.env", override=True)

from groq import Groq

def fetch_latest_spaceflight_news_articles():
    url = "https://api.spaceflightnewsapi.net/v4/articles"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        print(f"Failed to fetch SpaceFlight News articles: {err}")
        return None

def summarize_articles_to_heroic_update(articles_json):
    if not articles_json or "results" not in articles_json:
        return "No articles available to summarize."

    articles_info = ""
    for article in articles_json.get("results", []):
        title = article.get("title", "")
        summary = article.get("summary", "")
        articles_info += f"Title: {title}\nSummary: {summary}\n\n"

    prompt = (
        "Compose a short, inspiring 'heroic space update' for the public, summarizing the following news articles. "
        "Make it optimistic, adventurous, and dramatic, as if narrating the latest bold exploits of humanity in space!\n\n"
        f"{articles_info}"
    )

    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Failed to generate heroic summary: {e}"