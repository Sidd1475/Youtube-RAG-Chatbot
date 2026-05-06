def build_prompt(query, retrieved_chunks, history = None):
    
    context = ""

    for i , chunk in enumerate(retrieved_chunks):
        trimmed_text = chunk["text"][:300]
        context += f"""

[Source {i+1}]
Time : {chunk['start']:.2f}s - {chunk['end']:.2f}s
Content: {trimmed_text}
"""
      #  Build history 
    history_text = ""
    if history:
        history_text = "\n".join(
            [f"{m['role']}: {m['content']}" for m in history[-5:]]
        )  
        prompt = f"""
You are an Intelligent assistant.

Answer the question using ONLY the context below.
If the answer is not in the context, say "Not mentioned in video".

Conversation History:{history_text}
Context:{context}
Question:{query}

Instructions :
- Give a clear answer 
- Mention relevant timestamps 
- Avoid guessing
- Cite sources like [Source 1], [Source 2]

Answer:
"""
    return prompt
    