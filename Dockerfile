FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Luôn cài bản yt-dlp mới nhất — X.com thay đổi API thường xuyên
RUN pip install --no-cache-dir -U yt-dlp

WORKDIR /app

ENV PYTHONUNBUFFERED=1
