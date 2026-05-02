# ИНСТРУКЦИЯ ДЛЯ BOTHOST.RU

## Проблема
Бот собирается и подключается к голосовым каналам, но выдает ошибку:
```
discord.errors.ClientException: ffmpeg was not found.
```

## Причина
Хост bothost.ru не может загрузить `ffmpeg.exe` через репозиторий (exe файлы не загружаются).

## Решение

### Вариант 1: Docker (РЕКОМЕНДУЕТСЯ)
Docker автоматически установит ffmpeg внутри контейнера.

**Шаги:**
1. Убедитесь, что на bothost.ru есть Docker
2. Соберите образ:
   ```bash
   docker build -t jmusic-bot .
   ```
3. Запустите контейнер:
   ```bash
   docker run -d \
     --name jmusic-bot \
     --restart unless-stopped \
     -e DISCORD_TOKEN="ВАШ_ТОКЕН" \
     jmusic-bot
   ```

**Преимущества:**
- Автоматическая установка ffmpeg
- Изолированное окружение
- Легкое обновление

### Вариант 2: Установка ffmpeg на хосте
Попросите администратора bothost.ru установить ffmpeg:

**Для Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Для CentOS/RHEL:**
```bash
sudo yum install ffmpeg
```

**Проверка установки:**
```bash
ffmpeg -version
```

### Вариант 3: Использование системного ffmpeg
Если ffmpeg уже установлен на хосте, но бот его не находит:

1. Проверьте путь к ffmpeg:
   ```bash
   which ffmpeg
   ```

2. Обновите `bot.py` чтобы использовать правильный путь:
   ```python
   # В файле bot.py измените:
   FFMPEG_EXE = '/usr/bin/ffmpeg'  # или путь, который покажет which ffmpeg
   ```

## Проверка решения

После применения решения проверьте:

1. **Docker вариант:**
   ```bash
   docker exec jmusic-bot ffmpeg -version
   ```

2. **Ручная установка:**
   ```bash
   ffmpeg -version
   ```

3. **Запустите бота и проверьте команду `/play`**

## Файлы в репозитории

Для работы необходимы:
- ✅ `Dockerfile` - для Docker деплоя
- ✅ `requirements.txt` - Python зависимости  
- ✅ `bot.py` - основной код
- ✅ `.env.example` - шаблон конфигурации
- ✅ `config.json` - альтернативная конфигурация

## Если проблема осталась

1. Проверьте логи:
   ```bash
   docker logs jmusic-bot
   ```

2. Проверьте, что ffmpeg действительно установлен:
   ```bash
   # В контейнере
   docker exec jmusic-bot which ffmpeg
   
   # На хосте
   which ffmpeg
   ```

3. Проверьте права доступа:
   ```bash
   ls -la /usr/bin/ffmpeg
   ```

## Контакты для bothost.ru
Если нужна помощь с установкой ffmpeg на хосте, обратитесь к администратору bothost.ru.