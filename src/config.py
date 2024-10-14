import os
from dotenv import load_dotenv

load_dotenv()


MODEL_PATH = os.getenv("MODEL_PATH")
TRANSCRIPTION_MODEL = os.getenv("TRANSCRIPTION_MODEL")
VOSK_PATH_RU = os.getenv("VOSK_PATH_RU")
VOSK_PATH_EN = os.getenv("VOSK_PATH_EN")
WHISPER_MODEL_PATH = os.getenv("WHISPER_MODEL_PATH")
WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL_NAME")
LANGUAGE = os.getenv("LANGUAGE")