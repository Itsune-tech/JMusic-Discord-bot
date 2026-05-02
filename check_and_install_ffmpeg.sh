#!/bin/bash
# Скрипт для проверки и установки ffmpeg на bothost.ru

echo "🔧 ПРОВЕРКА И УСТАНОВКА FFMPEG ДЛЯ JMUSIC BOT"
echo "=============================================="

# Проверяем, запущен ли скрипт с правами root
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  Скрипт требует прав администратора (sudo)"
    echo "Запустите: sudo bash $0"
    exit 1
fi

# Проверка ОС
echo "🔍 Определение операционной системы..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "ОС: $NAME $VERSION"
else
    echo "Не удалось определить ОС"
fi

echo ""

# Проверка наличия ffmpeg
echo "🔍 Проверка установленного ffmpeg..."
if command -v ffmpeg &> /dev/null; then
    ffmpeg_version=$(ffmpeg -version | head -n1)
    ffmpeg_path=$(which ffmpeg)
    echo "✅ FFmpeg уже установлен:"
    echo "   Версия: $ffmpeg_version"
    echo "   Путь: $ffmpeg_path"
    exit 0
else
    echo "❌ FFmpeg не установлен"
fi

echo ""

# Установка в зависимости от ОС
echo "🔧 Установка ffmpeg..."

case $ID in
    ubuntu|debian)
        echo "Установка для Ubuntu/Debian..."
        apt-get update
        apt-get install -y ffmpeg
        ;;
        
    centos|rhel|fedora)
        echo "Установка для CentOS/RHEL/Fedora..."
        if command -v dnf &> /dev/null; then
            dnf install -y ffmpeg
        elif command -v yum &> /dev/null; then
            yum install -y ffmpeg
        else
            echo "❌ Не найден пакетный менеджер (dnf/yum)"
        fi
        ;;
        
    alpine)
        echo "Установка для Alpine Linux..."
        apk add ffmpeg
        ;;
        
    *)
        echo "❌ Неподдерживаемая ОС: $ID"
        echo "Установите ffmpeg вручную:"
        echo "https://ffmpeg.org/download.html"
        exit 1
        ;;
esac

echo ""

# Проверка после установки
echo "🔍 Проверка установки..."
if command -v ffmpeg &> /dev/null; then
    ffmpeg_version=$(ffmpeg -version | head -n1)
    ffmpeg_path=$(which ffmpeg)
    echo "✅ FFmpeg успешно установлен:"
    echo "   Версия: $ffmpeg_version"
    echo "   Путь: $ffmpeg_path"
    
    echo ""
    echo "📋 Информация для настройки бота:"
    echo "Бот будет искать ffmpeg по пути: $ffmpeg_path"
    echo "Если бот всё ещё не находит ffmpeg, проверьте:"
    echo "1. Что путь $ffmpeg_path существует"
    echo "2. Что у бота есть права на чтение/выполнение"
    echo "3. Или укажите путь явно в bot.py:"
    echo "   FFMPEG_EXE = '$ffmpeg_path'"
else
    echo "❌ FFmpeg не установлен после попытки установки"
    echo "Попробуйте установить вручную:"
    echo "https://ffmpeg.org/download.html"
fi

echo ""
echo "=============================================="
echo "✅ Установка завершена"
echo "Теперь бот должен работать с командой /play"