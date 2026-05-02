@echo off
echo 🔍 ПРОВЕРКА ВЕРСИЙ FFMPEG
echo =========================

echo Проверка Windows ffmpeg.exe...
if exist ffmpeg.exe (
    echo ✅ ffmpeg.exe найден
    for %%f in (ffmpeg.exe) do (
        set size=%%~zf
        set /a size_kb=!size!/1024
        echo   Размер: !size_kb! KB
    )
    
    echo   Проверка работоспособности...
    ffmpeg.exe -version 2>nul
    if errorlevel 1 (
        echo   ⚠️ ffmpeg.exe не работает
    ) else (
        echo   ✅ ffmpeg.exe работает
    )
) else (
    echo ❌ ffmpeg.exe не найден
)

echo.

echo Проверка Linux ffmpeg...
if exist ffmpeg (
    echo ✅ Linux ffmpeg найден (без расширения)
    for %%f in (ffmpeg) do (
        set size=%%~zf
        set /a size_kb=!size!/1024
        echo   Размер: !size_kb! KB
    )
    
    echo   Примечание: Linux ffmpeg требует Linux окружения
    echo   или WSL для работы на Windows
) else (
    echo ❌ Linux ffmpeg не найден
)

echo.

echo Проверка ffplay...
if exist ffplay (
    echo ✅ ffplay найден
    for %%f in (ffplay) do (
        set size=%%~zf
        set /a size_mb=!size!/1048576
        echo   Размер: !size_mb! MB
    )
) else (
    echo ❌ ffplay не найден
)

echo.

echo Проверка ffprobe...
if exist ffprobe (
    echo ✅ ffprobe найден
    for %%f in (ffprobe) do (
        set size=%%~zf
        set /a size_kb=!size!/1024
        echo   Размер: !size_kb! KB
    )
) else (
    echo ❌ ffprobe не найден
)

echo.
echo =========================
echo 📊 ИТОГ
echo =========================

if exist ffmpeg.exe (
    echo ✅ Windows ffmpeg.exe готов к использованию
) else (
    echo ❌ Windows ffmpeg.exe отсутствует
)

if exist ffmpeg (
    echo ✅ Linux ffmpeg присутствует
    echo ⚠️  Требуется Linux окружение для использования
) else (
    echo ❌ Linux ffmpeg отсутствует
)

echo.
echo Бот автоматически выберет правильную версию ffmpeg
echo в зависимости от окружения (Windows/Linux/Docker)
echo.
pause