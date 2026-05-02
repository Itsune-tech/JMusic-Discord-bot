# Деплой JMusic Discord Bot на bothost.ru

## Требования для хоста bothost.ru

1. Хост может запустить только `bot.py`
2. Все зависимости должны быть установлены через `requirements.txt`
3. Токен бота должен передаваться через переменную окружения `DISCORD_TOKEN`

## Шаги деплоя

### 1. Подготовка файлов

На хосте bothost.ru должны быть следующие файлы:
- `bot.py` - основной файл бота
- `requirements.txt` - зависимости
- `config.json` - конфигурация (опционально, если используется переменная окружения)
- `.env` - переменные окружения (опционально)

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Настройка токена бота

Создайте переменную окружения `DISCORD_TOKEN`:

```bash
export DISCORD_TOKEN="ваш_токен_бота"
```

Или создайте файл `.env`:
```
DISCORD_TOKEN=ваш_токен_бота
```

### 4. Запуск бота

```bash
python bot.py
```

## Решение проблем

### Ошибка: "davey library needed in order to use voice"

Эта ошибка возникает из-за отсутствия библиотеки `PyNaCl`. Убедитесь, что:
1. В `requirements.txt` указана версия `discord.py[voice]>=2.3.0`
2. Библиотека `PyNaCl` установлена: `pip install pynacl`

### Ошибка: "ffmpeg not found"

Установите ffmpeg на системе:
```bash
# Для Ubuntu/Debian
sudo apt-get install ffmpeg

# Для CentOS/RHEL
sudo yum install ffmpeg
```

### Ошибка: "python-dotenv not installed"

Установите библиотеку:
```bash
pip install python-dotenv
```

## Автоматический запуск

Для автоматического запуска на bothost.ru можно использовать:

1. **Systemd service** (для Linux):
```bash
sudo nano /etc/systemd/system/jmusic-bot.service
```

Содержимое файла:
```
[Unit]
Description=JMusic Discord Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/bot
Environment="DISCORD_TOKEN=your_token"
ExecStart=/usr/bin/python3 /path/to/bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. **Запуск через screen/tmux**:
```bash
screen -S jmusic-bot -dm python bot.py
```

## Мониторинг

Логи бота выводятся в консоль. Для сохранения логов в файл:

```bash
python bot.py >> bot.log 2>&1
```

## Обновление бота

1. Остановите бота
2. Обновите файлы
3. Установите обновленные зависимости:
```bash
pip install -r requirements.txt --upgrade
```
4. Запустите бота снова