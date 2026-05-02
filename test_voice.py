#!/usr/bin/env python3
"""
Тестовый скрипт для проверки голосовых зависимостей бота
"""

import sys
import os

print("=" * 60)
print("🔊 ТЕСТ ГОЛОСОВЫХ ЗАВИСИМОСТЕЙ")
print("=" * 60)

# Проверяем основные зависимости
dependencies = [
    ("discord.py", "discord"),
    ("PyNaCl", "nacl"),
    ("yt-dlp", "yt_dlp"),
    ("gTTS", "gtts"),
    ("ffmpeg-python", "ffmpeg"),
    ("python-dotenv", "dotenv")
]

all_ok = True
for package_name, import_name in dependencies:
    try:
        if import_name == "ffmpeg":
            import ffmpeg
        else:
            __import__(import_name)
        print(f"✅ {package_name} установлен")
    except ImportError as e:
        print(f"❌ {package_name} НЕ УСТАНОВЛЕН: {e}")
        all_ok = False

print("=" * 60)

# Проверка версии discord.py
try:
    import discord
    print(f"Discord.py версия: {discord.__version__}")
    
    # Проверка поддержки голоса
    if discord.version_info >= (2, 0, 0):
        print("✅ Discord.py 2.x поддерживает голосовой функционал")
    else:
        print("⚠️ Discord.py устаревшей версии, обновите до 2.x")
except ImportError:
    print("❌ Discord.py не установлен")

print("=" * 60)

# Проверка ffmpeg
import subprocess
try:
    result = subprocess.run(['ffmpeg', '-version'], 
                          capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        version_line = result.stdout.split('\n')[0]
        print(f"✅ FFmpeg доступен: {version_line}")
    else:
        print("❌ FFmpeg не работает корректно")
except (subprocess.SubprocessError, FileNotFoundError) as e:
    print(f"❌ FFmpeg не найден: {e}")

print("=" * 60)

if all_ok:
    print("✅ Все зависимости установлены! Бот готов к работе.")
else:
    print("❌ Некоторые зависимости отсутствуют. Установите их:")
    print("   pip install -r requirements.txt")
    
print("=" * 60)