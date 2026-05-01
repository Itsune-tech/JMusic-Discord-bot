#!/bin/bash
# Скрипт установки FFmpeg на Linux-хосте

echo "Установка FFmpeg..."

# Проверяем, установлен ли уже FFmpeg
if command -v ffmpeg &> /dev/null; then
    echo "FFmpeg уже установлен: $(ffmpeg -version | head -n1)"
    exit 0
fi

# Устанавливаем в зависимости от дистрибутива
if [ -f /etc/debian_version ]; then
    # Debian/Ubuntu
    apt-get update
    apt-get install -y ffmpeg
elif [ -f /etc/redhat-release ]; then
    # CentOS/RHEL/Fedora
    yum install -y ffmpeg ffmpeg-devel
elif [ -f /etc/arch-release ]; then
    # Arch Linux
    pacman -Sy --noconfirm ffmpeg
else
    echo "Неизвестный дистрибутив Linux. Установите FFmpeg вручную."
    exit 1
fi

echo "FFmpeg успешно установлен!"