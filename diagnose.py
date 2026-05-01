#!/usr/bin/env python3
"""
Диагностический скрипт для проверки установленных пакетов
"""

import subprocess
import sys

def check_package(package):
    """Проверить установлен ли пакет"""
    try:
        result = subprocess.run(
            [sys.executable, "-c", f"import {package}; print('✅ {package} установлен')"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True
    except:
        pass
    return False

def get_package_version(package):
    """Получить версию пакета"""
    try:
        result = subprocess.run(
            [sys.executable, "-c", f"import {package}; print({package}.__version__)"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    return "НЕ УСТАНОВЛЕН"

print("=" * 60)
print("ДИАГНОСТИКА УСТАНОВЛЕННЫХ ПАКЕТОВ")
print("=" * 60)

# Критически важные пакеты
critical_packages = [
    "discord",
    "nacl",
    "yt_dlp",
    "gtts"
]

print("\n🔍 Критически важные пакеты:")
all_ok = True
for pkg in critical_packages:
    if check_package(pkg):
        version = get_package_version(pkg)
        print(f"  ✅ {pkg}: {version}")
    else:
        print(f"  ❌ {pkg}: НЕ УСТАНОВЛЕН")
        all_ok = False

print("\n📦 Все установленные пакеты:")
try:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list"],
        capture_output=True,
        text=True
    )
    print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
except:
    print("Не удалось получить список пакетов")

print("\n" + "=" * 60)
if all_ok:
    print("✅ Все критические пакеты установлены")
    print("Проблема может быть в конфигурации или версиях")
else:
    print("❌ Отсутствуют критические пакеты")
    print("\nРЕШЕНИЕ:")
    print("1. Установите недостающие пакеты:")
    print("   pip install discord.py yt-dlp pynacl gtts")
    print("2. Или запустите: python install_deps.py")
print("=" * 60)