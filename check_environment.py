#!/usr/bin/env python3
"""
Скрипт для проверки окружения на хосте bothost.ru
Проверяет наличие всех необходимых зависимостей и ffmpeg
"""

import os
import sys
import subprocess
import platform

print("=" * 70)
print("🔍 ПРОВЕРКА ОКРУЖЕНИЯ ДЛЯ JMUSIC DISCORD BOT")
print("=" * 70)

# Проверка Python версии
print(f"Python версия: {sys.version}")
print(f"Платформа: {platform.platform()}")
print(f"Текущая директория: {os.getcwd()}")
print()

# Проверка наличия ffmpeg
print("🔧 ПРОВЕРКА FFMPEG")
print("-" * 40)

# Проверяем разные возможные пути к ffmpeg
ffmpeg_paths = [
    "ffmpeg",  # Системный
    "/usr/bin/ffmpeg",
    "/usr/local/bin/ffmpeg",
    "ffmpeg.exe",  # Windows
    "./ffmpeg.exe",  # Локальный
    "../ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"  # В родительской папке
]

ffmpeg_found = False
for path in ffmpeg_paths:
    try:
        result = subprocess.run([path, '-version'], 
                               capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg найден: {path}")
            print(f"   Версия: {version_line}")
            ffmpeg_found = True
            break
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        continue

if not ffmpeg_found:
    print("❌ FFmpeg не найден!")
    print("   Установите ffmpeg:")
    print("   - Ubuntu/Debian: sudo apt-get install ffmpeg")
    print("   - CentOS/RHEL: sudo yum install ffmpeg")
    print("   - Windows: скачайте с https://ffmpeg.org/download.html")
    print("   Или поместите ffmpeg.exe в текущую папку")

print()

# Проверка Node.js/Deno для yt-dlp
print("🔧 ПРОВЕРКА JAVASCRIPT RUNTIME ДЛЯ YT-DLP")
print("-" * 40)

# Проверяем Node.js
try:
    result = subprocess.run(['node', '--version'], 
                           capture_output=True, text=True, timeout=3)
    if result.returncode == 0:
        print(f"✅ Node.js найден: {result.stdout.strip()}")
    else:
        print("⚠️ Node.js не работает корректно")
except (subprocess.SubprocessError, FileNotFoundError):
    print("❌ Node.js не найден")

# Проверяем Deno
try:
    result = subprocess.run(['deno', '--version'], 
                           capture_output=True, text=True, timeout=3)
    if result.returncode == 0:
        print(f"✅ Deno найден: {result.stdout.split()[0]}")
    else:
        print("⚠️ Deno не работает корректно")
except (subprocess.SubprocessError, FileNotFoundError):
    print("❌ Deno не найден")

print()

# Проверка Python зависимостей
print("🔧 ПРОВЕРКА PYTHON ЗАВИСИМОСТЕЙ")
print("-" * 40)

dependencies = [
    ("discord.py", "discord"),
    ("PyNaCl", "nacl"),
    ("yt-dlp", "yt_dlp"),
    ("gTTS", "gtts"),
    ("ffmpeg-python", "ffmpeg"),
    ("python-dotenv", "dotenv")
]

all_deps_ok = True
for package_name, import_name in dependencies:
    try:
        if import_name == "ffmpeg":
            import ffmpeg
        else:
            __import__(import_name)
        print(f"✅ {package_name} установлен")
    except ImportError as e:
        print(f"❌ {package_name} НЕ УСТАНОВЛЕН: {e}")
        all_deps_ok = False

print()

# Проверка переменных окружения
print("🔧 ПРОВЕРКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ")
print("-" * 40)

discord_token = os.environ.get('DISCORD_TOKEN')
if discord_token:
    masked_token = discord_token[:10] + "..." + discord_token[-5:] if len(discord_token) > 15 else "***"
    print(f"✅ DISCORD_TOKEN установлен: {masked_token}")
else:
    print("❌ DISCORD_TOKEN не установлен!")
    print("   Установите переменную окружения:")
    print("   export DISCORD_TOKEN='ваш_токен_бота'")
    print("   Или создайте файл .env с DISCORD_TOKEN=ваш_токен_бота")

print()

# Итог
print("=" * 70)
print("📊 ИТОГ ПРОВЕРКИ")
print("=" * 70)

if ffmpeg_found and all_deps_ok and discord_token:
    print("✅ ВСЕ СИСТЕМНЫЕ ТРЕБОВАНИЯ ВЫПОЛНЕНЫ!")
    print("   Бот готов к запуску: python bot.py")
elif not ffmpeg_found:
    print("❌ ПРОБЛЕМА: FFmpeg не найден")
    print("   Бот не сможет воспроизводить музыку без ffmpeg")
elif not all_deps_ok:
    print("❌ ПРОБЛЕМА: Не все Python зависимости установлены")
    print("   Установите: pip install -r requirements.txt")
elif not discord_token:
    print("❌ ПРОБЛЕМА: DISCORD_TOKEN не установлен")
    print("   Установите переменную окружения или создайте .env файл")
else:
    print("⚠️ ЕСТЬ ПРОБЛЕМЫ С ОКРУЖЕНИЕМ")

print("=" * 70)