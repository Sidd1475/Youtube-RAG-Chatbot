import faiss 
import numpy as np
import os
import pickle

class VectorStore:
    def __init__(self, dim):
        self.dim = dim

        # FAISS Index (L2 distance)
        self.index = faiss.IndexFlatIP(dim)

        # store metadata seperately 
        self.metadata = []
    
    def add(self, embeddings_data):
        vectors = []

        for item in embeddings_data:
            vectors.append(item["embedding"])
            self.metadata.append(item)
            
        vectors = np.array(vectors).astype("float32")

        self.index.add(vectors)
    
    def search(self, query_vector, top_k = 5):
        query_vector = np.array([query_vector]).astype("float32")

        distances , indices = self.index.search(query_vector, top_k)

        results = []
        for i,idx in enumerate(indices[0]):
            if idx == -1:
                continue

            if idx < len(self.metadata):
                results.append({
                    "text": self.metadata[idx]["text"],
                    "start":self.metadata[idx]["start"],
                    "end":self.metadata[idx]["end"],
                    "score":float(distances[0][i])
                })

        return results    
    
    def save(self, path = "data/faiss"):
        os.makedirs(path, exist_ok = True)

        faiss.write_index(self.index , f"{path}/index.faiss")

        with open(f"{path}/metadata.pkl","wb") as f:
            pickle.dump(self.metadata, f)

        print("FAISS index saved")

    def load(self, path = "data/faiss"):
        self.index = faiss.read_index(f"{path}/index.faiss")

        with open(f"{path}/metadata.pkl","rb") as f:
            self.metadata = pickle.load(f)
        
        print("FAISS index loaded")
