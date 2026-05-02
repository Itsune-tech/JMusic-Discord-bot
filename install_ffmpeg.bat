@echo off
echo 🔧 Установка FFmpeg для JMusic Discord Bot
echo ==========================================

REM Проверяем наличие ffmpeg в системе
where ffmpeg >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ FFmpeg уже установлен в системе
    ffmpeg -version | findstr /C:"ffmpeg version"
    goto :end
)

REM Проверяем локальный ffmpeg.exe
if exist ffmpeg.exe (
    echo ✅ Локальный ffmpeg.exe найден в текущей папке
    goto :end
)

REM Проверяем ffmpeg в родительской папке
if exist ..\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe (
    echo ✅ FFmpeg найден в родительской папке
    goto :end
)

echo ❌ FFmpeg не найден!
echo.
echo Варианты установки:
echo 1. Скачайте ffmpeg с https://ffmpeg.org/download.html
echo    и поместите ffmpeg.exe в текущую папку
echo.
echo 2. Используйте Chocolatey (администратор):
echo    choco install ffmpeg
echo.
echo 3. Используйте Scoop:
echo    scoop install ffmpeg
echo.
echo 4. Установите вручную и добавьте в PATH
echo.

:end
pause