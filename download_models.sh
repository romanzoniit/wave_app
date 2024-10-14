#!/bin/bash

MODEL_DIR="/mnt/d/models"
VOSK_MODEL_EN_URL="https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
VOSK_MODEL_RU_URL="https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip"
WHISPER_MODEL_URL="https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt"
WHISPER_MODEL_DIR="$MODEL_DIR/whisper"


mkdir -p "$MODEL_DIR"
mkdir -p "$WHISPER_MODEL_DIR"

download_file() {
  local url="$1"
  local path="$2"
  if [ ! -f "$path" ]; then
    echo "Downloading $url to $path..."
    wget -O "$path" "$url"
    echo "Downloaded $path."
  else
    echo "File $path already exists, skipping download."
  fi
}

download_file "$VOSK_MODEL_EN_URL" "$MODEL_DIR/vosk-model-small-en-us-0.15.zip"

download_file "$VOSK_MODEL_RU_URL" "$MODEL_DIR/vosk-model-small-ru-0.22.zip"

download_file "$WHISPER_MODEL_URL" "$WHISPER_MODEL_DIR/base.pt"

unzip $MODEL_DIR/vosk-model-small-ru-0.22.zip -d $MODEL_DIR
unzip $MODEL_DIR/vosk-model-small-en-us-0.15.zip -d $MODEL_DIR