import os

from cosmic_agent import ask_cosmic_agent
from knowledge_engine import index_mission_data


def build_mission_index():
    """
    Index mission facts from mission_info.txt into ChromaDB.
    """
    mission_file = "mission_info.txt"
    if not os.path.exists(mission_file):
        raise FileNotFoundError(
            f"{mission_file} was not found. Add it to the project root first."
        )

    index_mission_data(mission_file)


def run_query_loop():
    """
    Ask user questions and answer them via RAG (ChromaDB retrieval + Gemini generation).
    """
    print("Cosmic Scientific Advisor is ready. Type 'exit' to stop.")
    while True:
        user_question = input("\nAsk a mission question: ").strip()
        if user_question.lower() in {"exit", "quit"}:
            print("Session ended.")
            break
        if not user_question:
            print("Please enter a question.")
            continue

        answer = ask_cosmic_agent(user_question)
        print(f"\nScientific Advisor: {answer}")


if __name__ == "__main__":
    build_mission_index()
    run_query_loop()
