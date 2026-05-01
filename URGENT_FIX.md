# СРОЧНЫЙ ФИКС ДЛЯ BOTHOST.RU

## Проблема
Бот запускается, но выдает ошибку:
```
RuntimeError: davey library needed in order to use voice
```

## Причина
**PyNaCl не установлен** на хосте. Без PyNaCl голосовой функционал Discord не работает.

## Решение

### Шаг 1: Изменить Build Command
В панели bothost.ru в Build Command добавьте:

```bash
# Устанавливаем ВСЕ зависимости вручную
pip install discord.py pynacl yt-dlp gtts ffmpeg-python

# Или используйте скрипт
python install_now.py
```

### Шаг 2: Или использовать этот Build Command полностью
```bash
echo "=== Установка зависимостей ==="
pip install discord.py
pip install pynacl
pip install yt-dlp
pip install gtts
pip install ffmpeg-python
echo "=== Зависимости установлены ==="
python bot.py
```

### Шаг 3: Проверка
После сборки в логах должно быть:
```
✅ discord.py установлен
✅ PyNaCl установлен!
✅ yt-dlp установлен
✅ gTTS установлен
✅ ffmpeg-python установлен
```

## Почему это происходит?
Bothost.ru не устанавливает зависимости из `requirements.txt` правильно. Нужно устанавливать их вручную.

## Если не помогло

### Обратитесь в поддержку bothost.ru:
```
Тема: Не устанавливаются зависимости Python

Сообщение:
Здравствуйте! Мой Discord бот не работает из-за отсутствия PyNaCl.

Проблема:
1. requirements.txt содержит: discord.py PyNaCl yt-dlp gTTS ffmpeg-python
2. Но зависимости не устанавливаются при сборке
3. Бот выдает ошибку "davey library needed in order to use voice"

Решение:
Разрешите установку зависимостей через pip в Build Command:
pip install discord.py pynacl yt-dlp gtts ffmpeg-python

Без PyNaCl голосовой функционал Discord не работает.
```

## Альтернатива
Если не удается решить, используйте другой хостинг:
- Railway.app (автоматически устанавливает зависимости)
- Heroku (с правильным buildpack)
- VPS (полный контроль)