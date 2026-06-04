import yt_dlp
import os

def download_audio(video_id):

    os.makedirs("temp", exist_ok=True)

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    output_template = "temp/audio.%(ext)s"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    for file in os.listdir("temp"):
        if file.startswith("audio"):
            return os.path.join("temp", file)

    raise Exception("Audio download failed")