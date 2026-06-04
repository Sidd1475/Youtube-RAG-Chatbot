from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq()

def transcribe_audio(audio_path):

    with open(audio_path, "rb") as audio_file:

        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3"
        )

    return transcription.text