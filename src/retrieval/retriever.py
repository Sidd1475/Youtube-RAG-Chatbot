import numpy as np 

def cosine_similarity(a,b):
    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))

def retrieve(query, embedded_data , embedder , top_k = 3):
    # step 1 : convert query to vector
    query_vec = embedder.generate_embeddings([query])[0]

    scores = []

    # Step 2 : compare with all chunks 
    for item in embedded_data:
        score = cosine_similarity(query_vec, item["embedding"])
        scores.append((score,item))
    
    # Step 3 : sort by similarity
    scores.sort(key=lambda x:x[0], reverse = True)

    # Step 4 : return top_k
    return [item for _, item in scores[:top_k]]