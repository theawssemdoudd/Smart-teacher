import re
import subprocess
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from youtube_transcript_api import YouTubeTranscriptApi
import whisper

app = FastAPI()

# استخدم نموذج Whisper صغير لتقليل الحجم
model = whisper.load_model("tiny")

def download_audio(video_url, out_name="audio.wav"):
    """تنزيل الصوت من يوتيوب وتحويله إلى wav"""
    cmd = f'yt-dlp -f bestaudio -x --audio-format wav -o "{out_name}" "{video_url}"'
    subprocess.run(cmd, shell=True, check=True)
    return out_name

@app.get("/transcribe")
async def transcribe(url: str = Query(..., description="رابط فيديو يوتيوب")):
    try:
        # استخراج video id
        m = re.search(r"(?:v=|\/youtu\.be\/)([A-Za-z0-9_\-]{6,})", url)
        if not m:
            return JSONResponse(content={"error": "رابط غير صالح"}, status_code=400)
        video_id = m.group(1)

        # 1) جرب transcript جاهز من يوتيوب
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ar', 'en'])
            text = " ".join([t['text'] for t in transcript])
            return {"source": "youtube_transcript", "text": text}
        except:
            # 2) لو مافيش ترجمة → نستعمل Whisper
            audio_path = download_audio(url, "audio.wav")
            result = model.transcribe(audio_path)
            text = result.get("text", "")
            return {"source": "whisper", "text": text}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
