#!/bin/bash
# Скрипт для тестирования Docker окружения

echo "🔧 ТЕСТИРОВАНИЕ DOCKER ОКРУЖЕНИЯ"
echo "================================="

# Собираем Docker образ
echo "1. Сборка Docker образа..."
docker build -t jmusic-bot-test .

echo ""
echo "2. Запуск тестового контейнера..."
docker run --rm -it jmusic-bot-test bash -c "
echo '=== Проверка внутри контейнера ==='
echo 'Проверка ffmpeg:'
which ffmpeg
ffmpeg -version | head -1
echo ''
echo 'Проверка Python зависимостей:'
python -c 'import discord; import nacl; import yt_dlp; from gtts import gTTS; import ffmpeg; print(\"✅ Все зависимости работают\")'
echo ''
echo 'Проверка Node.js/Deno:'
node --version 2>/dev/null || echo 'Node.js не найден'
deno --version 2>/dev/null || echo 'Deno не найден'
echo ''
echo 'Проверка bot.py:'
python -c '
import os
import subprocess

# Проверка поиска ffmpeg
print(\"🔍 Проверка поиска ffmpeg:\")
paths = [\"ffmpeg\", \"/usr/bin/ffmpeg\", \"/usr/local/bin/ffmpeg\", \"ffmpeg.exe\"]
for path in paths:
    try:
        result = subprocess.run([path, \"-version\"], capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            print(f\"  ✅ {path} работает\")
        else:
            print(f\"  ❌ {path} не работает\")
    except:
        print(f\"  ❌ {path} не найден\")
'
"

echo ""
echo "3. Запуск бота в тестовом режиме..."
docker run --rm -e DISCORD_TOKEN="test_token" jmusic-bot-test python -c "
import os
import sys
sys.path.insert(0, '/app')

# Имитируем запуск бота без реального подключения к Discord
print('=== ТЕСТОВЫЙ ЗАПУСК БОТА ===')
print('Проверка импортов...')

try:
    import discord
    import nacl
    import yt_dlp
    from gtts import gTTS
    import ffmpeg
    from dotenv import load_dotenv
    print('✅ Все импорты работают')
except Exception as e:
    print(f'❌ Ошибка импорта: {e}')

print('')
print('Проверка поиска ffmpeg из bot.py...')
exec(open('/app/bot.py').read().split('FFMPEG_EXE =')[0])
print(f'FFMPEG_EXE будет установлен в: {FFMPEG_EXE if \"FFMPEG_EXE\" in locals() else \"Не определен\"}')
"

echo ""
echo "✅ Тестирование завершено"
echo "Если все проверки пройдены, Docker образ готов к использованию на bothost.ru"