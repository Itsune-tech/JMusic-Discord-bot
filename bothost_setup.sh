#!/bin/bash
# Скрипт специально для bothost.ru
# Решает проблему с PyNaCl

echo "=== Настройка для bothost.ru ==="
echo "Проблема: PyNaCl не устанавливается автоматически"
echo "Решение: Принудительная установка системных зависимостей"

# Устанавливаем системные зависимости для PyNaCl
echo "1. Устанавливаю системные зависимости..."
apt-get update
apt-get install -y \
    libffi-dev \
    libssl-dev \
    libsodium-dev \
    build-essential \
    2>/dev/null || echo "⚠️ Не удалось установить системные зависимости"

# Устанавливаем PyNaCl отдельно
echo "2. Устанавливаю PyNaCl..."
pip install pynacl --no-cache-dir

# Проверяем
echo "3. Проверяю установку..."
python -c "import nacl; print('✅ PyNaCl установлен!')" || {
    echo "❌ PyNaCl не установлен!"
    echo "Попробую альтернативный метод..."
    pip install nacl --no-cache-dir
}

echo "4. Устанавливаю остальные зависимости..."
pip install -r requirements.txt

echo "=== Готово! ==="
echo "Бот должен работать с голосовым функционалом."