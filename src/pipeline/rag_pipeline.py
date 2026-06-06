import os
import json

from src.ingestion.youtube_loader import get_transcript
from src.ingestion.preprocess import preprocess
from src.indexing.chunker import chunk_text
from src.indexing.embedder import EmbeddingManager
from src.indexing.vector_store import VectorStore
from src.generation.prompt_builder import build_prompt
from src.generation.llm import GeminiGenerator
from deep_translator import GoogleTranslator
from youtube_transcript_api._errors import RequestBlocked, VideoUnavailable

class RAGPipeline:
    def __init__(self, api_key):
        self.embedder = EmbeddingManager()
        self.generator = GeminiGenerator(api_key)
        self.translator = GoogleTranslator(source='auto',target='en')

        self.index_path = "data/faiss"
        self.processed_file = "data/processed_video.json"
        # Load or create vector store 
        # if os.path.exists(f"{self.index_path}/index.faiss"):
        #     print("Loading FAISS index..")
        #     self.vector_store = VectorStore(dim=384)
        #     self.vector_store.load(self.index_path)
        # else:
        print("Creating a new FAISS index..")
        self.vector_store = None
        
        # Load processed video 
        if os.path.exists(self.processed_file):
            try:
                with open(self.processed_file, "r") as f:
                    self.processed_videos = set(json.load(f))
            except json.JSONDecodeError:
                    print("⚠️ JSON empty/corrupt → resetting")
                    self.processed_videos = set()
        else:
            self.processed_videos = set()

    #PROCESS VIDEO
    def process_video(self, video_id, language="en"):
        
        print(f"Processing Video: {video_id}")
        self.index_path = f"data/faiss/{video_id}"
        os.makedirs(self.index_path, exist_ok=True)
        # IMPORTANT: Reset vector store for every new video
        self.vector_store = None

        transcript = None
        languages_to_try = [language, "en", "hi"]

        for lang in languages_to_try:
            try:
                transcript = get_transcript(video_id, languages=[lang])
                if transcript:
                    break
            except RequestBlocked:
                raise RuntimeError("TRANSCRIPT_BLOCKED")
            except VideoUnavailable:
                continue
            except Exception as e:
                print(f"Transcript Error: {e}")
                raise
            
        #if still fails 
        if not transcript:
            raise RuntimeError("TRANSCRIPT_FAILED")
        
        for entry in transcript:
            try:
                entry["text"] = self.translator.translate(entry["text"])
            except Exception as e:
                print(f"Translation failed: {e}")
        
        
        cleaned = preprocess(transcript)
        chunks = chunk_text(cleaned)

        embedded_data = self.embedder.embed_chunks(chunks)
        
        # create vector stor if first time 
        if self.vector_store is None:
            dim = len(embedded_data[0]["embedding"])
            self.vector_store = VectorStore(dim)
        
        self.vector_store.add(embedded_data)
        self.vector_store.save(self.index_path)

        # self.processed_videos.add(video_id)
        # self._save_processed()

        print(f"VIDEO ID = {video_id}")
        print(f"INDEX PATH = {self.index_path}")

    # Query 
    def rewrite_query(self, question , history):
        if not history or len(history) < 2:
           return question
        
        prev_user_msgs = [m["content"] for m in history if m["role"] == "user"]
        if len(prev_user_msgs)<2:
            return question 
        
        prev_question = prev_user_msgs[-2]
        return prev_question+" "+question
    
    
    def query(self, question, history=[]):
        
        history_text = "\n".join(
        [f"{m['role']}: {m['content']}" for m in history[-5:]]
        )

        if history:
            question = self.rewrite_query(question, history)

        query_vec = self.embedder.generate_embeddings([question])[0]
        
        if self.vector_store is None:
           return "Video not processed properly. Please try again.", []

        retrieved_chunks = self.vector_store.search(query_vec)

        # Deduplication 
        seen = set()
        unique_chunks = []

        for chunk in retrieved_chunks:
            if chunk["text"] not in seen:
                unique_chunks.append(chunk)
                seen.add(chunk["text"])

        retrieved_chunks = unique_chunks[:3]

        prompt = build_prompt(question, retrieved_chunks, history)
        
        try:
            answer = self.generator.generate(prompt)
        except RuntimeError as e:
            if str(e)=="MODEL_BUSY":
                return "Model is currently busy please try again in a few second.",[]
            else :
                return "Something went wrong. Please try again.", []

        print(f"Querying from index path = {self.index_path}")
        return answer , retrieved_chunks
    
        
    
    # Save processed videos 

    def _save_processed(self):
        with open(self.processed_file, "w") as f:
           json.dump(list(self.processed_videos), f)
    
