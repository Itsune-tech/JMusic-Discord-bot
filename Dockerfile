FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libffi-dev \
    libssl-dev \
    libsodium-dev \
    build-essential \
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

# Проверяем установку
RUN python -c "import discord; import nacl; print('Discord.py:', discord.__version__)"

# Запускаем бота
CMD ["python", "bot.py"]