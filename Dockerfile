FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libffi-dev \
    libssl-dev \
    libsodium-dev \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Проверяем установку голосовых зависимостей
RUN python -c "import discord; import nacl; import yt_dlp; from gtts import gTTS; import ffmpeg; from dotenv import load_dotenv; print('✅ Все зависимости установлены:')" && \
    python -c "print('Discord.py:', discord.__version__); print('PyNaCl:', nacl.__version__ if hasattr(nacl, '__version__') else 'OK')"

# Запускаем бота
CMD ["python", "bot.py"]