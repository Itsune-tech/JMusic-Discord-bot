#!/usr/bin/env python3
"""
Скрипт для гарантированной установки зависимостей Discord бота
Запускать на хосте перед запуском бота
"""

import subprocess
import sys
import os

def run_command(cmd):
    """Выполнить команду и вывести результат"""
    print(f"🚀 Выполняю: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Ошибка: {result.stderr}")
        return False
    print(f"✅ Успешно: {result.stdout[:100]}...")
    return True

def main():
    print("=" * 60)
    print("Установка зависимостей для JMusic Discord Bot")
    print("=" * 60)
    
    # 1. Обновляем pip
    if not run_command("python -m pip install --upgrade pip"):
        print("Не удалось обновить pip, продолжаем...")
    
    # 2. Устанавливаем discord.py с голосовой поддержкой
    print("\n📦 Устанавливаю discord.py[voice]...")
    deps = [
        "discord.py[voice]>=2.3.0",
        "yt-dlp>=2024.1.1",
        "PyNaCl>=1.5.0",
        "nacl>=1.5.0",
        "gTTS>=2.5.0",
        "ffmpeg-python>=0.2.0"
    ]
    
    for dep in deps:
        cmd = f"python -m pip install --no-cache-dir {dep}"
        if not run_command(cmd):
            print(f"⚠️ Не удалось установить {dep}, пробую альтернативу...")
            # Альтернатива для PyNaCl
            if "PyNaCl" in dep or "nacl" in dep:
                run_command("python -m pip install pynacl")
    
    # 3. Проверяем установку
    print("\n🔍 Проверяю установку...")
    check_cmds = [
        "python -c \"import discord; print(f'Discord.py: {discord.__version__}')\"",
        "python -c \"import nacl; print('PyNaCl: OK')\"",
        "python -c \"import yt_dlp; print('yt-dlp: OK')\"",
        "python -c \"import gtts; print('gTTS: OK')\""
    ]
    
    for cmd in check_cmds:
        run_command(cmd)
    
    print("\n" + "=" * 60)
    print("✅ Установка завершена!")
    print("Запустите бота: python bot.py")
    print("=" * 60)

if __name__ == "__main__":
    main()