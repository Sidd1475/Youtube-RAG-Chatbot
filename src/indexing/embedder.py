from sentence_transformers import SentenceTransformer 
import numpy as np

class EmbeddingManager:
    def __init__(self , model_name="all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        self.model = SentenceTransformer(self.model_name)

    def generate_embeddings(self,texts):
        embeddings = self.model.encode(
            texts,
            show_progress_bar = True,
            normalize_embeddings = True
        )
        return embeddings
    
    def embed_chunks(self, chunks):
        texts = [chunk["text"] for chunk in chunks]
        vectors = self.generate_embeddings(texts)

        embedded_data = []

        for i in range(len(chunks)):
            embedded_data.append({
                "text":chunks[i]["text"],
                "embedding":vectors[i],
                "start":chunks[i]["start"],
                 "end":chunks[i]["end"]
            })
        
        return embedded_data