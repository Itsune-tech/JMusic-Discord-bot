# JMusic Discord Bot - Деплой на bothost.ru

## Краткое описание

Этот бот предоставляет функционал воспроизведения музыки в Discord с поддержкой:
- Воспроизведение музыки с YouTube и других платформ
- Управление очередью воспроизведения
- Система плейлистов
- TTS (текст в речь)
- Голосовые команды

## Быстрый старт для bothost.ru

### 1. Клонирование репозитория
```bash
git clone <репозиторий>
cd "JMusic Discord bot"
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка токена бота

**Вариант A: Через переменную окружения**
```bash
export DISCORD_TOKEN="ваш_токен_бота"
```

**Вариант B: Через файл .env**
```bash
echo "DISCORD_TOKEN=ваш_токен_бота" > .env
```

**Вариант C: Через config.json**
Отредактируйте `config.json`:
```json
{
    "api_key": "ваш_токен_бота",
    "prefix": "/"
}
```

### 4. Запуск бота
```bash
python bot.py
```

## Решение проблем

### Ошибка: "davey library needed in order to use voice"
Установите PyNaCl:
```bash
pip install pynacl
```

И убедитесь, что в requirements.txt указано:
```
discord.py[voice]>=2.3.0
PyNaCl>=1.5.0
```

### Ошибка: "ffmpeg not found"
Установите ffmpeg:
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg

# Windows
# Скачайте с https://ffmpeg.org/download.html
# Или используйте локальный ffmpeg.exe из папки
```

### Ошибка: "python-dotenv not installed"
```bash
pip install python-dotenv
```

## Тестирование зависимостей
```bash
python test_voice.py
```

## Запуск на Windows
```bash
run_bothost.bat
```

## Docker деплой
```bash
docker build -t jmusic-bot .
docker run -e DISCORD_TOKEN="ваш_токен" jmusic-bot
```

## Команды бота

- `/play <запрос>` - Воспроизвести музыку
- `/pause` - Поставить на паузу
- `/unpause` - Продолжить воспроизведение
- `/stop` - Остановить и выйти из канала
- `/skip` - Пропустить текущий трек
- `/queue` - Показать очередь
- `/tts <текст>` - Озвучить текст
- `/playlist` - Управление плейлистами

## Поддержка
Для проблем с деплоем на bothost.ru обратитесь к файлу `DEPLOY_BOTHOST.md`