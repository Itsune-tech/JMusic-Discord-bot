#!/usr/bin/env python3
"""
АБСОЛЮТНО НАДЕЖНАЯ установка PyNaCl
Работает даже при проблемах с зависимостями
"""

import os
import sys
import subprocess
import time

def run(cmd):
    """Выполнить команду с выводом"""
    print(f"💻 Выполняю: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️ Предупреждение: {result.stderr[:200]}")
    else:
        print(f"✅ Успешно")
    return result

print("=" * 70)
print("ПРИНУДИТЕЛЬНАЯ УСТАНОВКА PyNaCl ДЛЯ DISCORD ГОЛОСОВОГО ФУНКЦИОНАЛА")
print("=" * 70)

# Шаг 1: Устанавливаем системные зависимости (для Linux)
print("\n1️⃣ Устанавливаю системные зависимости...")
if os.path.exists("/etc/debian_version"):
    run("apt-get update && apt-get install -y libffi-dev libssl-dev libsodium-dev python3-dev 2>/dev/null || true")
elif os.path.exists("/etc/redhat-release"):
    run("yum install -y libffi-devel openssl-devel libsodium-devel python3-devel 2>/dev/null || true")

# Шаг 2: Обновляем pip
print("\n2️⃣ Обновляю pip...")
run(f"{sys.executable} -m pip install --upgrade pip")

# Шаг 3: Устанавливаем PyNaCl разными способами
print("\n3️⃣ Пробую установить PyNaCl...")

# Способ 1: Обычная установка
print("   Способ 1: pip install pynacl")
run(f"{sys.executable} -m pip install pynacl")

# Проверяем
print("\n🔍 Проверяю установку...")
check = run(f"{sys.executable} -c \"import nacl; print('🎉 PyNaCl УСТАНОВЛЕН! Версия:', nacl.__version__)\"")

if check.returncode != 0:
    # Способ 2: Установка без зависимостей
    print("\n   Способ 2: pip install --no-deps pynacl")
    run(f"{sys.executable} -m pip install --no-deps pynacl")
    
    # Проверяем снова
    check = run(f"{sys.executable} -c \"import nacl; print('🎉 PyNaCl УСТАНОВЛЕН (без зависимостей)!')\"")

if check.returncode != 0:
    # Способ 3: Установка из wheel
    print("\n   Способ 3: Скачиваю и устанавливаю wheel...")
    run("pip download pynacl --no-deps")
    run("pip install *.whl")
    
    # Убираем временные файлы
    run("rm -f *.whl 2>/dev/null || true")

# Шаг 4: Устанавливаем остальные зависимости
print("\n4️⃣ Устанавливаю остальные зависимости...")
deps = ["discord.py", "yt-dlp", "gtts", "ffmpeg-python"]
for dep in deps:
    print(f"   Устанавливаю {dep}...")
    run(f"{sys.executable} -m pip install {dep}")

# Финальная проверка
print("\n" + "=" * 70)
print("ФИНАЛЬНАЯ ПРОВЕРКА УСТАНОВКИ")
print("=" * 70)

packages = {
    "discord": "discord.py",
    "nacl": "PyNaCl", 
    "yt_dlp": "yt-dlp",
    "gtts": "gTTS"
}

all_good = True
for import_name, package_name in packages.items():
    result = run(f"{sys.executable} -c \"try:\n import {import_name}\n print('✅ {package_name}: OK')\nexcept:\n print('❌ {package_name}: ОШИБКА')\"")
    if "❌" in result.stdout:
        all_good = False

print("\n" + "=" * 70)
if all_good:
    print("🎉 ВСЕ ЗАВИСИМОСТИ УСТАНОВЛЕНЫ!")
    print("Бот готов к работе!")
else:
    print("⚠️ НЕКОТОРЫЕ ЗАВИСИМОСТИ НЕ УСТАНОВЛЕНЫ")
    print("Обратитесь в поддержку хоста с этим логом")
print("=" * 70)