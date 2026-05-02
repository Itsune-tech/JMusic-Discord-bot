#!/bin/bash
# Тестовый скрипт для проверки ffmpeg в Docker

echo "🔧 ТЕСТИРОВАНИЕ FFMPEG В DOCKER"
echo "================================"

echo "1. Проверка системного ffmpeg..."
if command -v ffmpeg &> /dev/null; then
    ffmpeg -version | head -1
    echo "✅ Системный ffmpeg работает"
else
    echo "❌ Системный ffmpeg не найден"
fi

echo ""
echo "2. Проверка локального Linux ffmpeg..."
if [ -f "ffmpeg" ]; then
    echo "✅ Локальный Linux ffmpeg найден"
    
    # Проверяем права
    if [ -x "ffmpeg" ]; then
        echo "✅ Файл имеет права на выполнение"
    else
        echo "⚠️ Файл не имеет прав на выполнение, устанавливаю..."
        chmod +x ffmpeg
    fi
    
    # Пробуем запустить
    echo "🔍 Проверка работоспособности..."
    ./ffmpeg -version 2>&1 | head -5
    if [ $? -eq 0 ]; then
        echo "✅ Локальный Linux ffmpeg работает"
    else
        echo "❌ Локальный Linux ffmpeg не работает (возможно, не хватает библиотек)"
    fi
else
    echo "❌ Локальный Linux ffmpeg не найден"
fi

echo ""
echo "3. Проверка библиотек..."
echo "🔍 Поиск библиотек libavdevice..."
find /usr/lib -name "libavdevice*" 2>/dev/null | head -3
find /lib -name "libavdevice*" 2>/dev/null | head -3

echo ""
echo "4. Проверка через ldd (только для Linux бинарников)..."
if [ -f "ffmpeg" ] && command -v ldd &> /dev/null; then
    echo "🔍 Проверка зависимостей локального ffmpeg:"
    ldd ffmpeg 2>/dev/null | grep -E "(not found|libavdevice)" || echo "  Все зависимости найдены или не удалось проверить"
fi

echo ""
echo "5. Проверка Python логики выбора ffmpeg..."
python3 -c "
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
IS_DOCKER = os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv')
IS_LINUX = sys.platform.startswith('linux')

print(f'IS_DOCKER: {IS_DOCKER}')
print(f'IS_LINUX: {IS_LINUX}')
print(f'Платформа: {sys.platform}')

# Пути для проверки
paths = [
    (os.path.join(_HERE, 'ffmpeg'), 'локальный Linux ffmpeg'),
    ('/usr/bin/ffmpeg', 'системный /usr/bin/ffmpeg'),
    ('/usr/local/bin/ffmpeg', 'системный /usr/local/bin/ffmpeg'),
    (os.path.join(_HERE, 'ffmpeg.exe'), 'Windows ffmpeg.exe'),
]

print('\\nПроверка путей:')
for path, desc in paths:
    exists = os.path.exists(path)
    print(f'{desc}: {\"✅ СУЩЕСТВУЕТ\" if exists else \"❌ НЕ СУЩЕСТВУЕТ\"}')
"

echo ""
echo "================================"
echo "📊 ИТОГ"
echo "================================"

if command -v ffmpeg &> /dev/null; then
    echo "✅ Системный ffmpeg доступен и должен работать"
    echo "   Бот будет использовать системный ffmpeg в Docker"
elif [ -f "ffmpeg" ] && [ -x "ffmpeg" ]; then
    echo "⚠️ Только локальный Linux ffmpeg доступен"
    echo "   Могут быть проблемы с библиотеками"
else
    echo "❌ FFmpeg не найден"
    echo "   Установите ffmpeg в Dockerfile"
fi

echo ""
echo "Для запуска бота в Docker:"
echo "docker build -t jmusic-bot ."
echo "docker run -e DISCORD_TOKEN='ваш_токен' jmusic-bot"