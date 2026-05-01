#!/bin/bash
# Скрипт установки для Linux-хоста

echo "=== Установка JMusic Discord Bot ==="

# Обновляем систему
echo "1. Обновление системы..."
apt-get update -y

# Устанавливаем системные зависимости
echo "2. Установка системных зависимостей..."
apt-get install -y \
    python3 \
    python3-pip \
    ffmpeg \
    libffi-dev \
    libssl-dev \
    libsodium-dev \
    python3-dev \
    build-essential

# Устанавливаем Python зависимости
echo "3. Установка Python зависимостей..."
pip3 install --upgrade pip
pip3 install discord.py>=2.3.0
pip3 install yt-dlp>=2024.1.1
pip3 install PyNaCl>=1.5.0
pip3 install gTTS>=2.5.0
pip3 install ffmpeg-python>=0.2.0

echo "4. Проверка установки..."
python3 -c "import discord; import nacl; print('✓ Discord.py:', discord.__version__); print('✓ PyNaCl установлен')"

echo "=== Установка завершена ==="
echo "Запуск бота: python3 bot.py"