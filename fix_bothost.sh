#!/bin/bash
# Фикс для bothost.ru - обход строгой проверки requirements.txt

echo "=== Фикс для bothost.ru ==="
echo "Проблема: система пропускает 'nacl' считая его встроенным модулем"

# Создаем временный requirements.txt без проблемных строк
echo "Создаю безопасный requirements.txt..."
cat > /tmp/safe_requirements.txt << EOF
discord.py
yt-dlp
pynacl
gtts
ffmpeg-python
python-dotenv
EOF

# Устанавливаем из безопасного файла
echo "Устанавливаю зависимости..."
pip install --no-cache-dir -r /tmp/safe_requirements.txt

# Проверяем PyNaCl отдельно (самый важный!)
echo "Проверяю PyNaCl..."
python -c "import nacl; print('✅ PyNaCl установлен!')" || {
    echo "❌ PyNaCl не установлен, устанавливаю принудительно..."
    pip install --no-cache-dir pynacl
}

echo "=== Фикс завершен ==="