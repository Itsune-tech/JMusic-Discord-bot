# ФИНАЛЬНЫЙ ФИКС ДЛЯ BOTHOST.RU

## Проблема 1: yt-dlp==2024.1.1 не существует
Bothost.ru не может найти версию `yt-dlp==2024.1.1`. Доступны только dev-версии.

## Проблема 2: PyNaCl не устанавливается
Система пропускает `nacl` считая его встроенным модулем.

## Решение:

### Шаг 1: Используйте правильный requirements.txt
Замените `requirements.txt` на:
```
discord.py
PyNaCl
yt-dlp
gTTS
ffmpeg-python
```

### Шаг 2: В панели bothost.ru
1. **Удалите старый requirements.txt** если он есть
2. **Используйте новый requirements.txt** (без версий)
3. **Или добавьте в Build Command:**
```bash
# Удаляем старый и создаем новый
rm -f requirements.txt
echo -e "discord.py\nPyNaCl\nyt-dlp\ngTTS\nffmpeg-python" > requirements.txt

# Устанавливаем
pip install -r requirements.txt
```

### Шаг 3: Проверка
После сборки в логах должно быть:
```
✅ Успешно установлен: discord.py
✅ Успешно установлен: PyNaCl  
✅ Успешно установлен: yt-dlp
✅ Успешно установлен: gTTS
✅ Успешно установлен: ffmpeg-python
```

## Почему это работает:
1. **Без версий** = pip установит последние доступные версии
2. **PyNaCl** (с большой P) не попадает под фильтр "встроенных модулей"
3. **yt-dlp** без версии установит последнюю доступную

## Если сборка всё ещё падает:
1. **Свяжитесь с поддержкой bothost.ru**
2. **Сообщите:** "Ваш скрипт сборки не находит yt-dlp==2024.1.1 и пропускает PyNaCl"
3. **Попросите:** разрешить установку без строгой проверки версий

## Альтернатива: Docker
Если есть возможность использовать Docker:
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y ffmpeg
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

С `requirements.txt`:
```
discord.py
PyNaCl
yt-dlp
gTTS
ffmpeg-python
```