#!/bin/bash
# Скрипт для установки прав доступа на Linux ffmpeg файлы

echo "🔧 УСТАНОВКА ПРАВ ДОСТУПА ДЛЯ LINUX FFMPEG"
echo "=========================================="

# Проверяем, что мы в Linux
if [[ "$OSTYPE" != "linux-gnu"* ]] && [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️ Этот скрипт предназначен для Linux/macOS"
    echo "Текущая ОС: $OSTYPE"
    exit 1
fi

# Файлы для настройки
FILES=("ffmpeg" "ffplay" "ffprobe")

echo "Проверка файлов..."
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ Найден: $file"
        
        # Проверяем текущие права
        current_perms=$(stat -c "%A" "$file")
        echo "   Текущие права: $current_perms"
        
        # Проверяем, есть ли право на выполнение
        if [[ ! "$current_perms" =~ "x" ]]; then
            echo "   ⚠️ Нет права на выполнение, устанавливаю..."
            chmod +x "$file"
            new_perms=$(stat -c "%A" "$file")
            echo "   ✅ Новые права: $new_perms"
        else
            echo "   ✅ Права на выполнение уже установлены"
        fi
        
        # Проверяем владельца
        owner=$(stat -c "%U:%G" "$file")
        echo "   Владелец: $owner"
        
    else
        echo "❌ Не найден: $file"
    fi
done

echo ""
echo "🔍 Проверка работоспособности ffmpeg..."
if [ -f "ffmpeg" ]; then
    ./ffmpeg -version | head -1
    if [ $? -eq 0 ]; then
        echo "✅ ffmpeg работает корректно"
    else
        echo "❌ ffmpeg не работает"
    fi
else
    echo "⚠️ ffmpeg не найден"
fi

echo ""
echo "🔍 Проверка работоспособности ffplay..."
if [ -f "ffplay" ]; then
    ./ffplay -version 2>&1 | head -1
    if [ $? -eq 0 ]; then
        echo "✅ ffplay работает корректно"
    else
        echo "⚠️ ffplay может требовать дополнительных зависимостей"
    fi
else
    echo "⚠️ ffplay не найден"
fi

echo ""
echo "🔍 Проверка работоспособности ffprobe..."
if [ -f "ffprobe" ]; then
    ./ffprobe -version 2>&1 | head -1
    if [ $? -eq 0 ]; then
        echo "✅ ffprobe работает корректно"
    else
        echo "❌ ffprobe не работает"
    fi
else
    echo "⚠️ ffprobe не найден"
fi

echo ""
echo "=========================================="
echo "📊 ИТОГ"
echo "=========================================="

if [ -f "ffmpeg" ] && [ -x "ffmpeg" ]; then
    echo "✅ Linux ffmpeg готов к использованию"
    echo "   Бот будет использовать локальный Linux ffmpeg"
else
    echo "❌ Проблема с Linux ffmpeg"
    echo "   Убедитесь, что файл ffmpeg существует и имеет права на выполнение"
fi

echo ""
echo "Для запуска бота: python bot.py"