# Инструкция для bothost.ru

## Проблема
Discord бот выдает ошибку: `RuntimeError: davey library needed in order to use voice`

## Причина
Хостинг bothost.ru не устанавливает PyNaCl (библиотеку для голосового шифрования Discord) из-за отсутствия системных зависимостей.

## Решение для панели bothost.ru

### Вариант A: Использовать Docker (рекомендуется)
1. В панели bothost.ru выберите **Docker** как метод развертывания
2. Используйте `Dockerfile.bothost` из репозитория
3. Или укажите этот Dockerfile:
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y ffmpeg libffi-dev libssl-dev libsodium-dev build-essential
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

### Вариант B: Добавить скрипт установки
1. Добавьте **Pre-build script** в настройках:
```bash
#!/bin/bash
apt-get update
apt-get install -y libffi-dev libssl-dev libsodium-dev build-essential
pip install pynacl
```

### Вариант C: Ручная установка (если есть SSH доступ)
```bash
# Подключитесь по SSH к bothost.ru
cd /app  # или ваша директория

# Установите системные зависимости
apt-get update
apt-get install -y libffi-dev libssl-dev libsodium-dev build-essential

# Переустановите зависимости
pip install -r requirements.txt --force-reinstall

# Перезапустите бота
```

## Настройки для bothost.ru

### 1. Build Command (если используется обычная сборка):
```bash
apt-get update && apt-get install -y libffi-dev libssl-dev libsodium-dev build-essential && pip install -r requirements.txt
```

### 2. Start Command:
```bash
python bot.py
```

### 3. Environment Variables:
- `DISCORD_TOKEN` = ваш_токен_дискорд_бота

## Проверка работы

После настройки проверьте:
1. Бот должен подключиться к Discord
2. Команда `/play` должна работать без ошибки `davey library`
3. Бот должен подключаться к голосовым каналам

## Если проблема осталась

1. **Свяжитесь с поддержкой bothost.ru** и отправьте им эту инструкцию
2. **Попросите установить системные пакеты**:
   - `libffi-dev`
   - `libssl-dev` 
   - `libsodium-dev`
   - `build-essential`
3. **Или разрешите использовать Docker** с полным контролем над окружением

## Контакты поддержки
- Сайт: https://bothost.ru
- Поддержка: support@bothost.ru (или через панель управления)

## Альтернатива
Если не удается решить проблему на bothost.ru, рассмотрите альтернативные хостинги:
- Railway.app (имеет FFmpeg и PyNaCl по умолчанию)
- Heroku (с buildpack для Python)
- VPS (полный контроль)