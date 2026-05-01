#!/bin/bash
# Скрипт запуска бота с проверкой зависимостей

echo "🔍 Проверка зависимостей..."

# Проверяем Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден"
    exit 1
fi

# Проверяем зависимости
echo "📦 Проверяю Python зависимости..."
python3 -c "
try:
    import discord
    print('✅ discord.py:', discord.__version__)
except ImportError:
    print('❌ discord.py не установлен')
    exit(1)

try:
    import nacl
    print('✅ PyNaCl установлен')
except ImportError:
    print('❌ PyNaCl не установлен')
    print('Установите: pip install pynacl')
    exit(1)

try:
    import yt_dlp
    print('✅ yt-dlp установлен')
except ImportError:
    print('❌ yt-dlp не установлен')
    exit(1)
"

# Проверяем FFmpeg
echo "🎵 Проверяю FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg: $(ffmpeg -version | head -n1 | awk '{print $3}')"
else
    echo "⚠️ FFmpeg не найден. Голосовой функционал может не работать."
fi

echo "🚀 Запускаю бота..."
python3 bot.py