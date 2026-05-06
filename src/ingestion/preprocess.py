def clean_text(text):
    text = text.replace("\n"," ")
    text = text.strip()
    return text

def preprocess(transcript):
    processed = []
    for entry in transcript:
        cleaned = clean_text(entry["text"])

        if(len(cleaned)>20):
            processed.append({
                "text":cleaned,
                "start":entry["start"],
                "end":entry["end"]
            })
        
    return processed