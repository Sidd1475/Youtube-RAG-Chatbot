def chunk_text(data, chunk_size=300, overlap=50):
    chunks = []
    current_chunk = ""
    current_start = data[0]["start"]

    for entry in data:
        text = entry["text"]

        if len(current_chunk) + len(text) < chunk_size:
            current_chunk += " " + text
        else:
            chunks.append({
                "text": current_chunk.strip(),
                "start": current_start,
                "end": entry["end"]
            })

            # overlap
            current_chunk = current_chunk[-overlap:]
            current_chunk += " " + text
            current_start = entry["start"]

    return chunks