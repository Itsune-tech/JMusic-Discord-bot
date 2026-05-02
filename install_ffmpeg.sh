#!/bin/bash
# Скрипт для установки ffmpeg на разных системах

echo "🔧 Установка FFmpeg для JMusic Discord Bot"
echo "=========================================="

# Определяем ОС
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Обнаружена Linux система"
    
    # Проверяем дистрибутив
    if [ -f /etc/debian_version ]; then
        echo "Debian/Ubuntu система"
        sudo apt-get update
        sudo apt-get install -y ffmpeg
    elif [ -f /etc/redhat-release ]; then
        echo "RHEL/CentOS система"
        sudo yum install -y ffmpeg
    elif [ -f /etc/arch-release ]; then
        echo "Arch Linux система"
        sudo pacman -S ffmpeg
    else
        echo "Неизвестный дистрибутив Linux"
        echo "Установите ffmpeg вручную: https://ffmpeg.org/download.html"
    fi
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Обнаружена macOS система"
    brew install ffmpeg
    
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "Обнаружена Windows система"
    echo "Скачайте ffmpeg с https://ffmpeg.org/download.html"
    echo "Или используйте Chocolatey: choco install ffmpeg"
    echo "Или используйте Scoop: scoop install ffmpeg"
    
    # Проверяем наличие локального ffmpeg.exe
    if [ -f "ffmpeg.exe" ]; then
        echo "✅ Локальный ffmpeg.exe найден в текущей папке"
    else
        echo "⚠️ Локальный ffmpeg.exe не найден"
        echo "   Поместите ffmpeg.exe в текущую папку"
    fi
else
    echo "Неизвестная ОС: $OSTYPE"
    echo "Установите ffmpeg вручную: https://ffmpeg.org/download.html"
fi

echo ""
echo "Проверка установки ffmpeg..."
if command -v ffmpeg &> /dev/null; then
    ffmpeg_version=$(ffmpeg -version | head -n1)
    echo "✅ FFmpeg установлен: $ffmpeg_version"
else
    echo "❌ FFmpeg не найден в PATH"
    echo "   Проверьте установку или добавьте ffmpeg в PATH"
fi