from youtube_transcript_api import YouTubeTranscriptApi

from src.ingestion.audio_downloader import download_audio
from src.ingestion.whisper_loader import transcribe_audio

import os


def get_transcript(video_id, languages=["en", "hi", "es"]):

    try:
        api = YouTubeTranscriptApi()

        transcript = api.fetch(
            video_id,
            languages=languages
        )

        data = []

        for snippet in transcript.snippets:
            data.append(
                {
                    "text": snippet.text,
                    "start": snippet.start,
                    "end": snippet.start + snippet.duration
                }
            )

        print("Transcript API Success")

        return data

    except Exception as e:

        print(f"Transcript API Failed: {e}")
        print("Falling back to Groq Whisper...")

        try:
            audio_path = download_audio(video_id)

            transcript_text = transcribe_audio(audio_path)

        except Exception as e:
            print(f"Whisper Fallback Failed: {e}")
            raise

        if os.path.exists(audio_path):
            os.remove(audio_path)

        return [
            {
                "text": transcript_text,
                "start": 0,
                "end": 0
            }
        ]