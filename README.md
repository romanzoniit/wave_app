# WAVE APP
1. Скачаем и разархивируем модели для этого запустим скрипт `download_models.sh`

    ``sh download_models.sh``
2. В .env параметры запуска 
- Выберем язык `LANGUAGE = ru` или `LANGUAGE = en`
- Выберем модель распознавания речи `TRANSCRIPTION_MODEL = vosk` или `TRANSCRIPTION_MODEL = whisper`
3. В docker-compose настройки пути для моделей в volumes
4. Запустим и соберем docker-контейнер с помощью команды `docker-compose up --build`
5. При следующих запусках используем `docker-compose up`
6. После запуска заходим на 127.0.0.1:8000/docs
7. /modify_audio - ендпоинт для модификации аудио
8. /transcribe_audio - ендпоинт для распознавания речи
9. Расшифровка текста сохранится в /mnt/d/var/endpoints/transcribe 
10. Модифицированное аудио в /mnt/d/var/endpoints/audio

