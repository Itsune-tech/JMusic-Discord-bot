#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы с Linux ffmpeg
"""

import os
import sys
import subprocess
import stat

print("=" * 70)
print("🔧 ТЕСТИРОВАНИЕ LINUX FFMPEG")
print("=" * 70)

_HERE = os.path.dirname(os.path.abspath(__file__))

# Проверяем файлы
files_to_check = [
    ("ffmpeg.exe", "Windows ffmpeg"),
    ("ffmpeg", "Linux ffmpeg"),
    ("ffplay", "Linux ffplay"),
    ("ffprobe", "Linux ffprobe"),
]

print("🔍 ПРОВЕРКА ФАЙЛОВ:")
print("-" * 40)

for filename, description in files_to_check:
    filepath = os.path.join(_HERE, filename)
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        size_mb = size / (1024 * 1024)
        
        # Проверяем права для Linux файлов
        if filename in ["ffmpeg", "ffplay", "ffprobe"]:
            try:
                st = os.stat(filepath)
                is_executable = bool(st.st_mode & stat.S_IEXEC)
                perm_str = "✅ исполняемый" if is_executable else "❌ не исполняемый"
            except:
                perm_str = "⚠️ не удалось проверить права"
        else:
            perm_str = "Windows файл"
            
        print(f"{description}: {size_mb:.2f} MB, {perm_str}")
    else:
        print(f"{description}: ❌ не найден")

print()

# Тестируем логику выбора ffmpeg
print("🔍 ТЕСТИРОВАНИЕ ЛОГИКИ ВЫБОРА FFMPEG")
print("-" * 40)

# Определяем окружение
IS_DOCKER = os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv')
IS_LINUX = sys.platform.startswith('linux')
IS_WINDOWS = sys.platform.startswith('win')

print(f"Платформа: {sys.platform}")
print(f"IS_DOCKER: {IS_DOCKER}")
print(f"IS_LINUX: {IS_LINUX}")
print(f"IS_WINDOWS: {IS_WINDOWS}")

# Пути для проверки (как в bot.py)
paths_to_check = []

if IS_DOCKER or IS_LINUX:
    print("\nПриоритет для Linux/Docker:")
    paths_to_check = [
        (os.path.join(_HERE, 'ffmpeg'), "локальный Linux ffmpeg"),
        ('/usr/bin/ffmpeg', "системный /usr/bin/ffmpeg"),
        ('/usr/local/bin/ffmpeg', "системный /usr/local/bin/ffmpeg"),
        (os.path.join(_HERE, 'ffmpeg.exe'), "Windows ffmpeg.exe"),
    ]
else:
    print("\nПриоритет для Windows:")
    paths_to_check = [
        (os.path.join(_HERE, 'ffmpeg.exe'), "Windows ffmpeg.exe"),
        (os.path.join(_HERE, 'ffmpeg'), "Linux ffmpeg"),
        ('/usr/bin/ffmpeg', "системный /usr/bin/ffmpeg"),
        ('/usr/local/bin/ffmpeg', "системный /usr/local/bin/ffmpeg"),
    ]

print("\nПроверка путей в порядке приоритета:")
for i, (path, description) in enumerate(paths_to_check, 1):
    exists = os.path.exists(path)
    status = "✅ СУЩЕСТВУЕТ" if exists else "❌ НЕ СУЩЕСТВУЕТ"
    print(f"{i}. {description}: {status}")
    if exists:
        print(f"   Путь: {path}")

print()

# Проверка работоспособности
print("🔧 ПРОВЕРКА РАБОТОСПОСОБНОСТИ")
print("-" * 40)

# Проверяем первый найденный путь
ffmpeg_to_test = None
for path, description in paths_to_check:
    if os.path.exists(path):
        ffmpeg_to_test = path
        print(f"Тестируем: {description} ({path})")
        break

if ffmpeg_to_test:
    try:
        result = subprocess.run([ffmpeg_to_test, '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ Работает: {version_line}")
            
            # Проверка кодеков
            codec_check = subprocess.run([ffmpeg_to_test, '-codecs'], 
                                        capture_output=True, text=True, timeout=5)
            if 'libopus' in codec_check.stdout:
                print("✅ Поддерживается Opus кодек (нужен для Discord)")
            else:
                print("⚠️ Opus кодек не найден")
                
        else:
            print(f"❌ Не работает: {result.stderr[:200]}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
else:
    print("❌ Не найден ни один ffmpeg")

print()
print("=" * 70)
print("📊 ИТОГ")
print("=" * 70)

linux_ffmpeg_exists = os.path.exists(os.path.join(_HERE, 'ffmpeg'))
windows_ffmpeg_exists = os.path.exists(os.path.join(_HERE, 'ffmpeg.exe'))

if linux_ffmpeg_exists:
    print("✅ Linux ffmpeg найден в папке бота")
    if IS_LINUX or IS_DOCKER:
        print("✅ Бот будет использовать Linux ffmpeg")
    else:
        print("⚠️ Linux ffmpeg найден, но окружение не Linux")
        
if windows_ffmpeg_exists:
    print("✅ Windows ffmpeg.exe найден в папке бота")
    if IS_WINDOWS:
        print("✅ Бот будет использовать Windows ffmpeg.exe")
    else:
        print("⚠️ Windows ffmpeg.exe найден, но окружение не Windows")

if not linux_ffmpeg_exists and not windows_ffmpeg_exists:
    print("❌ Не найден ни Linux ffmpeg, ни Windows ffmpeg.exe")
    print("   Бот будет пытаться использовать системный ffmpeg")

print("=" * 70)