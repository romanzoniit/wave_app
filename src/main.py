import os
import shutil

from fastapi import FastAPI, UploadFile, File, Body, Form
from fastapi.responses import FileResponse

from src.models import AudioModificationRequest
from src.utils import modify_audio_file, transcribe_with_vosk, transcribe_with_whisper
from src.config import LANGUAGE, TRANSCRIPTION_MODEL


app = FastAPI()


@app.post("/modify_audio/")
async def modify_audio(speed: float = Form(1.0), volume: float = Form(1.0), file: UploadFile = File(...)):

    params = AudioModificationRequest(speed=speed, volume=volume)
    input_path = f"temp_{file.filename}"

    output_path = os.path.join("/endpoints/audio", f"modified_{file.filename}")

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    modify_audio_file(input_path, output_path, params)

    response = FileResponse(output_path, media_type='audio/wav', filename=f"modified_{file.filename}")
    response.headers['Content-Disposition'] = f'attachment; filename="{file.filename}"'

    return response



@app.post("/transcribe_audio/")
async def transcribe_audio(file: UploadFile = File(...)):
    input_path = f"temp_{file.filename}"
    transcription_result = {}

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if TRANSCRIPTION_MODEL == "vosk":
        transcription_result = transcribe_with_vosk(input_path, file)
    elif TRANSCRIPTION_MODEL == "whisper":
        transcription_result = transcribe_with_whisper(input_path, LANGUAGE, file)

    return transcription_result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)