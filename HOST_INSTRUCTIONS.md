# Инструкция для хоста

## Проблема
Бот выдает ошибку: `RuntimeError: davey library needed in order to use voice`

## Причина
Не установлена библиотека PyNaCl (pynacl) для голосового шифрования Discord.

## Решение

### Вариант 1: Быстрая установка (рекомендуется)
```bash
# На хосте выполните:
pip install discord.py yt-dlp pynacl gtts ffmpeg-python
```

### Вариант 2: Через requirements.txt
Убедитесь, что установлены все зависимости:
```bash
pip install -r requirements.txt
```

### Вариант 3: Используйте скрипт
```bash
python install_deps.py
```

### Вариант 4: Docker
Если поддерживается Docker:
```bash
docker build -t jmusic-bot .
docker run -e DISCORD_TOKEN=ваш_токен jmusic-bot
```

## Проверка
После установки проверьте:
```bash
python -c "import nacl; print('PyNaCl OK')"
python -c "import discord; print(f'Discord.py {discord.__version__}')"
```

## Если проблема осталась
1. Установите системные зависимости (для Linux):
   ```bash
   apt-get install -y libffi-dev libssl-dev libsodium-dev python3-dev
   ```
2. Переустановите PyNaCl:
   ```bash
   pip uninstall pynacl -y
   pip install pynacl --no-cache-dir
   ```

## Минимальные требования
- Python 3.8+
- PyNaCl (pynacl)
- discord.py
- FFmpeg (системный или в PATH)