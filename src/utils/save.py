import os 
import json 

def save_chunks(chunks, video_id):
    os.makedirs("data/processes",exist_ok=True)

    file_path = f'data/processed/{video_id}_chunks.json'
    with open(file_path,"w") as f:
        json.dump(chunks,f,indent = 2)
    
    print(f'Saved to {file_path}')