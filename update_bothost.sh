#!/bin/bash
# Скрипт для принудительного обновления bothost.ru

echo "=== Принудительное обновление bothost.ru ==="
echo "Проблема: bothost.ru использует старый кешированный requirements.txt"

# Создаем новый requirements.txt
echo "Создаю новый requirements.txt..."
cat > requirements.txt << 'EOF'
discord.py
PyNaCl
yt-dlp
gTTS
ffmpeg-python
EOF

echo "Содержимое нового requirements.txt:"
cat requirements.txt

echo ""
echo "=== Инструкция для bothost.ru ==="
echo "1. Добавьте в Build Command:"
echo "----------------------------------------"
echo "rm -f requirements.txt"
echo "echo -e \"discord.py\\\\nPyNaCl\\\\nyt-dlp\\\\ngTTS\\\\nffmpeg-python\" > requirements.txt"
echo "pip install -r requirements.txt"
echo "----------------------------------------"
echo ""
echo "2. Или пересоздайте проект чтобы сбросить кеш"
echo ""
echo "3. Или свяжитесь с поддержкой чтобы очистили кеш сборки"