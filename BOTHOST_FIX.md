# Критический фикс для bothost.ru

## Проблема
Bothost.ru имеет строгий скрипт сборки, который:
1. **Пропускает `nacl`** считая его встроенным модулем Python
2. **Не устанавливает PyNaCl** → голосовой функционал Discord не работает

## Решение

### Вариант 1: Использовать Docker (рекомендуется)
1. В настройках bothost.ru выберите **Docker**
2. Используйте `Dockerfile.bothost` из репозитория
3. Или скопируйте этот Dockerfile:

```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y ffmpeg libffi-dev libssl-dev libsodium-dev build-essential
WORKDIR /app
COPY . .
RUN echo -e "discord.py\nyt-dlp\npynacl\ngtts\nffmpeg-python\npython-dotenv" > safe_reqs.txt && \
    pip install --no-cache-dir -r safe_reqs.txt
CMD ["python", "bot.py"]
```

### Вариант 2: Изменить процесс сборки
Если Docker недоступен, добавьте в **Build Command**:

```bash
# Удалите старый requirements.txt и создайте безопасный
rm -f requirements.txt
echo -e "discord.py\nyt-dlp\npynacl\ngtts\nffmpeg-python\npython-dotenv" > requirements.txt

# Установите системные зависимости
apt-get update && apt-get install -y libffi-dev libssl-dev libsodium-dev build-essential

# Установите Python зависимости
pip install -r requirements.txt
```

### Вариант 3: Pre-build Script
Добавьте этот скрипт в **Pre-build Script**:

```bash
#!/bin/bash
# Фикс для bothost.ru
echo "=== Фикс для установки PyNaCl ==="

# Устанавливаем системные зависимости
apt-get update
apt-get install -y libffi-dev libssl-dev libsodium-dev build-essential

# Создаем безопасный requirements.txt
cat > /tmp/requirements_fixed.txt << EOF
discord.py
yt-dlp
pynacl
gtts
ffmpeg-python
python-dotenv
EOF

# Устанавливаем
pip install -r /tmp/requirements_fixed.txt

# Проверяем
python -c "import nacl; print('PyNaCl установлен')" || pip install pynacl
```

## Почему это происходит?
Bothost.ru проверяет `requirements.txt` и пропускает строки которые выглядят как встроенные модули Python.
Список пропускаемых модулей включает `nacl` (ошибочно).

## Проверка после фикса
После применения фикса:
1. В логах сборки должно появиться: `✅ PyNaCl установлен`
2. Бот должен запускаться без ошибки `davey library needed`
3. Команды `/play`, `/tts` должны работать

## Если не помогло
Свяжитесь с поддержкой bothost.ru и отправьте:
1. Эту инструкцию
2. Сообщение: "Ваш скрипт сборки пропускает `nacl` считая его встроенным модулем, но это внешняя библиотека PyNaCl необходимая для Discord голосового функционала"