#!/usr/bin/env python3
"""
Финальный тест ffmpeg для Discord бота
Показывает как бот использует ffmpeg
"""

import os
import sys
import subprocess

print("=" * 60)
print("🎵 ТЕСТ FFMPEG ДЛЯ DISCORD БОТА")
print("=" * 60)

# 1. Проверка что ffmpeg доступен
print("1. Проверка доступности ffmpeg:")
try:
    result = subprocess.run(['ffmpeg', '-version'], 
                          capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        version_line = result.stdout.split('\n')[0]
        print(f"   ✅ ffmpeg доступен: {version_line}")
        
        # Проверяем основные функции которые использует Discord бот
        print(f"\n2. Проверка функций нужных Discord боту:")
        
        # Проверяем поддержку MP3 (нужно для TTS)
        result2 = subprocess.run(['ffmpeg', '-formats'], 
                               capture_output=True, text=True, timeout=5)
        if 'mp3' in result2.stdout.lower():
            print(f"   ✅ Поддержка MP3: есть (нужно для TTS)")
        else:
            print(f"   ⚠️ Поддержка MP3: нет (TTS может не работать)")
            
        # Проверяем поддержку потокового аудио
        result3 = subprocess.run(['ffmpeg', '-protocols'], 
                               capture_output=True, text=True, timeout=5)
        if 'http' in result3.stdout.lower():
            print(f"   ✅ Поддержка HTTP потоков: есть (нужно для YouTube)")
        else:
            print(f"   ⚠️ Поддержка HTTP потоков: нет (/play может не работать)")
            
    else:
        error_msg = result.stderr[:200] if result.stderr else "нет ошибки"
        print(f"   ❌ ffmpeg не работает: {error_msg}")
except Exception as e:
    print(f"   ❌ Не удалось запустить ffmpeg: {e}")

# 2. Проверка локального файла /app/ffmpeg
print(f"\n3. Проверка локального /app/ffmpeg:")
if os.path.exists('/app/ffmpeg'):
    print("   ✅ /app/ffmpeg существует")
    try:
        result = subprocess.run(['/app/ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("   ✅ /app/ffmpeg работает")
        else:
            error_msg = result.stderr[:200] if result.stderr else "нет ошибки"
            print(f"   ❌ /app/ffmpeg не работает: {error_msg}")
            if 'libavdevice.so' in error_msg:
                print("   ⚠️ Проблема с библиотеками (ожидаемо в Docker)")
    except Exception as e:
        print(f"   ❌ Не удалось запустить /app/ffmpeg: {e}")
else:
    print("   ❌ /app/ffmpeg не существует")

print("\n" + "=" * 60)
print("📋 ВЫВОД:")
print("   Discord боту нужен РАБОЧИЙ ffmpeg в системе")
print("   В Docker: 'apt-get install ffmpeg' в Dockerfile")
print("   Бот использует 'ffmpeg' через PATH")
print("   Локальный /app/ffmpeg обычно не работает в Docker")
print("=" * 60)