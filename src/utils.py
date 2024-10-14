import os
import json
import librosa
import soundfile as sf
from vosk import Model, KaldiRecognizer
import whisper
import wave

from src.models import AudioModificationRequest
from src.config import MODEL_PATH, TRANSCRIPTION_MODEL, VOSK_PATH_EN, VOSK_PATH_RU, LANGUAGE, WHISPER_MODEL_PATH, WHISPER_MODEL_NAME



if TRANSCRIPTION_MODEL == "vosk":
    if LANGUAGE == "ru":
        VOSK_MODEL_PATH = f"{MODEL_PATH}{VOSK_PATH_RU}"
    elif LANGUAGE == "en":
        VOSK_MODEL_PATH = f"{MODEL_PATH}{VOSK_PATH_EN}"
    else:
        raise ValueError("Unsupported language specified for Vosk model.")
    if not os.path.exists(VOSK_MODEL_PATH):
        raise ValueError("Vosk model not found at specified path.")
    model = Model(VOSK_MODEL_PATH)
elif TRANSCRIPTION_MODEL == "whisper":
    whisper_model = whisper.load_model(WHISPER_MODEL_NAME, download_root=WHISPER_MODEL_PATH)
else:
    raise ValueError("Invalid transcription model specified. Use 'vosk' or 'whisper'.")


def modify_audio_file(input_path: str, output_path: str, params: AudioModificationRequest):
    # Load audio
    audio_data, sample_rate = librosa.load(input_path, sr=None)

    # Modify speed
    if params and params.speed != 1.0:
        audio_data = librosa.effects.time_stretch(audio_data, rate=params.speed)

    # Modify volume
    if params and params.volume != 1.0:
        audio_data = audio_data * params.volume

    # Save modified audio
    sf.write(output_path, audio_data, sample_rate)


def transcribe_with_vosk(input_path, file):
    wf = wave.open(input_path, "rb")
    if wf.getnchannels() != 1:
        raise ValueError("Audio file must be mono")

    recognizer = KaldiRecognizer(model, wf.getframerate())
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            results.append(json.loads(recognizer.Result()))
    results.append(json.loads(recognizer.FinalResult()))

    output_file = os.path.join("/endpoints/transcribe", f"transcription_{file.filename}.json")
    with open(output_file, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    return {"result": results}


def transcribe_with_whisper(input_path, language, file):
    result = whisper_model.transcribe(input_path, language=language)
    output_file = os.path.join("/endpoints/transcribe", f"transcription_{file.filename}.json")
    with open(output_file, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    return {"result": result}
