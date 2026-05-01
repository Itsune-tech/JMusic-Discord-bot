#!/usr/bin/env python3
"""
Скрипт для ПРИНУДИТЕЛЬНОЙ установки зависимостей на bothost.ru
Запускать в Build Command
"""

import subprocess
import sys

def run(cmd):
    """Выполнить команду"""
    print(f"💻 Выполняю: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️ Ошибка: {result.stderr[:200]}")
        return False
    print(f"✅ Успешно")
    return True

print("=" * 70)
print("ПРИНУДИТЕЛЬНАЯ УСТАНОВКА ЗАВИСИМОСТЕЙ ДЛЯ DISCORD БОТА")
print("=" * 70)

# 1. Устанавливаем ВСЕ зависимости по одной
dependencies = [
    "discord.py",
    "pynacl",      # Критически важно для голоса!
    "yt-dlp",
    "gtts",
    "ffmpeg-python"
]

print("\n📦 Устанавливаю зависимости...")
for dep in dependencies:
    print(f"\nУстанавливаю {dep}...")
    if not run(f"{sys.executable} -m pip install {dep}"):
        print(f"⚠️ Не удалось установить {dep}, пробую без кеша...")
        run(f"{sys.executable} -m pip install --no-cache-dir {dep}")

# 2. Проверяем установку
print("\n🔍 Проверяю установку...")
check_commands = [
    f'{sys.executable} -c "import discord; print(f\"✅ discord.py: {discord.__version__}\")"',
    f'{sys.executable} -c "import nacl; print(\"✅ PyNaCl установлен!\")"',
    f'{sys.executable} -c "import yt_dlp; print(\"✅ yt-dlp установлен\")"',
    f'{sys.executable} -c "import gtts; print(\"✅ gTTS установлен\")"',
    f'{sys.executable} -c "import ffmpeg; print(\"✅ ffmpeg-python установлен\")"'
]

for cmd in check_commands:
    run(cmd)

print("\n" + "=" * 70)
print("✅ УСТАНОВКА ЗАВЕРШЕНА")
print("=" * 70)
print("\nЕсли PyNaCl установлен, голосовой функционал Discord должен работать.")
print("Если нет - бот будет выдавать ошибку 'davey library needed'")