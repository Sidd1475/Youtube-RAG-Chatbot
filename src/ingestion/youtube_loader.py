from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id , languages=["en", "hi", "es"]):
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id , languages = languages)

    data = []
    for snippet in transcript.snippets:
        data.append({
            "text": snippet.text,
            "start": snippet.start,
            "end": snippet.start + snippet.duration
        })
    
    return data