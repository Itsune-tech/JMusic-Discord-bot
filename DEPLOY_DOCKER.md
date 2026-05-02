# Деплой через Docker на bothost.ru

## Преимущества Docker деплоя:
1. **Автоматическая установка ffmpeg** - не нужно устанавливать вручную
2. **Изолированное окружение** - все зависимости в контейнере
3. **Простота обновления** - просто пересобрать образ
4. **Консистентность** - одинаковое окружение на всех хостах

## Шаги деплоя:

### 1. Подготовка файлов
На bothost.ru должны быть следующие файлы:
- `Dockerfile` - инструкция сборки
- `requirements.txt` - Python зависимости
- `bot.py` - основной код бота
- `config.json` или `.env` - конфигурация
- (опционально) `docker-compose.yml` - для удобного запуска

### 2. Сборка Docker образа
```bash
docker build -t jmusic-bot .
```

### 3. Настройка переменных окружения
Создайте файл `.env` в той же папке:
```env
DISCORD_TOKEN=ваш_токен_бота
```

Или установите переменную окружения:
```bash
export DISCORD_TOKEN="ваш_токен_бота"
```

### 4. Запуск контейнера

**Вариант A: Через docker run**
```bash
docker run -d \
  --name jmusic-bot \
  --restart unless-stopped \
  -e DISCORD_TOKEN="ваш_токен_бота" \
  jmusic-bot
```

**Вариант B: Через docker-compose**
```bash
docker-compose up -d
```

### 5. Проверка работы
```bash
# Просмотр логов
docker logs jmusic-bot

# Проверка состояния
docker ps | grep jmusic-bot

# Вход в контейнер для отладки
docker exec -it jmusic-bot bash
```

## Решение проблем Docker

### Ошибка: "ffmpeg was not found"
Проверьте, что в Dockerfile есть:
```dockerfile
RUN apt-get update && apt-get install -y ffmpeg
```

И проверьте сборку:
```bash
docker build -t jmusic-bot-test . --no-cache
docker run --rm jmusic-bot-test ffmpeg -version
```

### Ошибка: "davey library needed"
Убедитесь, что в requirements.txt есть:
```
discord.py[voice]>=2.3.0
PyNaCl>=1.5.0
```

### Ошибка: недостаточно памяти
Добавьте в docker-compose.yml:
```yaml
services:
  jmusic-bot:
    mem_limit: 512m
    mem_reservation: 256m
```

## Автоматический перезапуск
Для автоматического перезапуска при падении:
```bash
docker run -d \
  --name jmusic-bot \
  --restart unless-stopped \
  -e DISCORD_TOKEN="ваш_токен" \
  jmusic-bot
```

## Мониторинг
```bash
# Статистика использования ресурсов
docker stats jmusic-bot

# Логи в реальном времени
docker logs -f jmusic-bot

# Проверка здоровья
docker inspect jmusic-bot --format='{{.State.Health.Status}}'
```

## Обновление бота
1. Остановите старый контейнер:
   ```bash
   docker stop jmusic-bot
   docker rm jmusic-bot
   ```

2. Обновите код

3. Пересоберите образ:
   ```bash
   docker build -t jmusic-bot .
   ```

4. Запустите заново

## Для bothost.ru специфично
Поскольку bothost.ru может запускать только `bot.py`, но поддерживает Docker:
1. Заливайте все файлы в репозиторий
2. На bothost.ru запускайте сборку Docker образа
3. Запускайте контейнер с переменной окружения `DISCORD_TOKEN`

Это гарантирует, что ffmpeg будет установлен корректно внутри контейнера, а не на хосте.