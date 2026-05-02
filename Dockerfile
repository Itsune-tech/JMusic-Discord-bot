FROM python:3.11-slim

# Устанавливаем системные зависимости для Discord бота и ffmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libavdevice-dev \
    libavformat-dev \
    libavcodec-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    libopus-dev \
    libsodium-dev \
    libffi-dev \
    libssl-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Проверяем что ffmpeg установлен и работает
RUN which ffmpeg && echo "✅ Системный FFmpeg установлен в: $(which ffmpeg)" \
    && ffmpeg -version | head -1 \
    && echo "✅ Все необходимые библиотеки ffmpeg установлены" \
    && echo "✅ Библиотека Opus установлена (для голосового чата Discord)"

# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Проверяем установку всех зависимостей
RUN echo "🔧 Проверка всех зависимостей..." && \
    python -c "import discord; import nacl; import yt_dlp; from gtts import gTTS; import ffmpeg; from dotenv import load_dotenv; print('✅ Все Python зависимости установлены')" && \
    python -c "print('Discord.py:', discord.__version__); print('PyNaCl:', nacl.__version__ if hasattr(nacl, '__version__') else 'OK')" && \
    echo "🔧 Проверка ffmpeg..." && \
    ffmpeg -version | head -3 && \
    echo "✅ FFmpeg работает корректно"

# Запускаем простой тест ffmpeg
RUN python test_ffmpeg_simple.py

# Запускаем бота
CMD ["python", "bot.py"]