import os
from src.pipeline.rag_pipeline import RAGPipeline
from dotenv import load_dotenv
load_dotenv()
def main():
    print("YouTube RAG CLI")

    pipeline = RAGPipeline(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    video_id = input("Enter YouTube Video ID: ")
    language = input("Enter language: ")
    
    pipeline.process_video(video_id , language)

    
    while True:
        query = input("\nAsk a question (or type 'exit'): ")

        if query.lower() == "exit":
            break

        answer, sources = pipeline.query(query)

        print("\n------ ANSWER ------\n")
        print(answer)

        print("\n------ SOURCES ------\n")
        for s in sources:
            print(f"{s['start']:.2f}s - {s['end']:.2f}s")
            print(s["text"][:200])
            print("-" * 40)


if __name__ == "__main__":
    main()