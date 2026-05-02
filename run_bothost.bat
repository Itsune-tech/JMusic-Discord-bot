@echo off
echo Запуск JMusic Discord Bot для хоста bothost.ru
echo ===============================================

REM Проверка наличия переменной окружения DISCORD_TOKEN
if "%DISCORD_TOKEN%"=="" (
    echo ОШИБКА: Переменная окружения DISCORD_TOKEN не установлена!
    echo Установите переменную окружения:
    echo set DISCORD_TOKEN=ваш_токен_бота
    echo Или создайте файл .env с содержимым:
    echo DISCORD_TOKEN=ваш_токен_бота
    pause
    exit /b 1
)

echo Проверка зависимостей...
python -c "import discord; import nacl; import yt_dlp; print('✅ Основные зависимости установлены')" 2>nul
if errorlevel 1 (
    echo Установка зависимостей...
    pip install -r requirements.txt
)

echo Проверка ffmpeg...
where ffmpeg >nul 2>nul
if errorlevel 1 (
    if exist ffmpeg.exe (
        echo ✅ Использую локальный ffmpeg.exe
    ) else (
        echo ❌ FFmpeg не найден!
        echo Бот не сможет воспроизводить музыку без ffmpeg.
        echo Запустите install_ffmpeg.bat для установки ffmpeg.
        echo.
        echo Продолжить без ffmpeg? (y/n)
        choice /c yn /n /m "Выберите действие:"
        if errorlevel 2 (
            echo Отмена запуска.
            pause
            exit /b 1
        )
    )
) else (
    echo ✅ FFmpeg найден в системе
)

echo.
echo Запуск бота...
python bot.py
pause