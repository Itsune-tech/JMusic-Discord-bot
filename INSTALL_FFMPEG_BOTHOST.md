# Установка ffmpeg на bothost.ru

## Проблема
Боту нужен ffmpeg для воспроизведения музыки, но:
1. ffmpeg.exe весит 193MB (слишком много для загрузки через репозиторий)
2. Ошибка: `Allowed memory size of 268435456 bytes exhausted`

## Решение

### Вариант 1: Установить ffmpeg на сервере (РЕКОМЕНДУЕТСЯ)
Попросите администратора bothost.ru установить ffmpeg:

**Для Linux (скорее всего bothost.ru использует Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Проверка установки:**
```bash
ffmpeg -version
which ffmpeg
```

**Пути, где бот будет искать ffmpeg:**
- `/usr/bin/ffmpeg`
- `/usr/local/bin/ffmpeg`
- `/opt/ffmpeg/bin/ffmpeg`

### Вариант 2: Использовать Docker
Если установить ffmpeg на сервере нельзя, используйте Docker:

```bash
# Сборка образа (установит ffmpeg внутри контейнера)
docker build -t jmusic-bot .

# Запуск
docker run -d --name jmusic-bot -e DISCORD_TOKEN="ваш_токен" jmusic-bot
```

### Вариант 3: Минимальная версия ffmpeg
Если нужно загрузить через репозиторий, используйте минимальную сборку:

1. Скачайте статический бинарник от BtbN:
   ```
   https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip
   ```

2. Распакуйте и возьмите только `ffmpeg.exe` (около 80MB)

3. Поместите в папку с ботом

### Вариант 4: Альтернативные пакетные менеджеры
Если на bothost.ru есть:
- **Snap:** `sudo snap install ffmpeg`
- **Flatpak:** `flatpak install flathub org.freedesktop.Platform.ffmpeg`
- **Homebrew:** `brew install ffmpeg`

## Проверка решения

После установки ffmpeg проверьте:

1. **Что ffmpeg доступен:**
   ```bash
   ffmpeg -version
   ```

2. **Где находится ffmpeg:**
   ```bash
   which ffmpeg
   ```

3. **Запустите проверочный скрипт:**
   ```bash
   python check_environment.py
   ```

## Если установка невозможна

Если нельзя установить ffmpeg на сервер, рассмотрите:

1. **Использование онлайн-сервиса** для конвертации аудио (менее надежно)
2. **Переход на другой хостинг** с поддержкой Docker
3. **Использование другого бота** без зависимости от ffmpeg

## Контактная информация
Для установки ffmpeg на bothost.ru обратитесь к администратору хоста с этой инструкцией.