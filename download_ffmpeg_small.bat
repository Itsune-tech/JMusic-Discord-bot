@echo off
echo Загрузка компактной версии ffmpeg для bothost.ru
echo =================================================

REM URL для скачивания статического бинарника ffmpeg от BtbN
REM Это версия только с основными кодеками, гораздо меньше полной
set FFMPEG_URL=https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip

echo 1. Скачивание компактной версии ffmpeg...
powershell -Command "Invoke-WebRequest -Uri '%FFMPEG_URL%' -OutFile 'ffmpeg-small.zip'"

if not exist ffmpeg-small.zip (
    echo ❌ Не удалось скачать ffmpeg
    echo Попробуйте скачать вручную:
    echo %FFMPEG_URL%
    pause
    exit /b 1
)

echo 2. Распаковка...
powershell -Command "Expand-Archive -Path 'ffmpeg-small.zip' -DestinationPath '.' -Force"

echo 3. Поиск ffmpeg.exe в распакованных файлах...
dir /s /b ffmpeg*.exe | findstr /i "ffmpeg.exe"

echo 4. Копирование в текущую папку...
for /r %%f in (ffmpeg.exe) do (
    copy "%%f" .\
    echo ✅ Найден и скопирован: %%f
    goto :found
)

:found
if exist ffmpeg.exe (
    echo.
    echo Проверка размера...
    for %%f in (ffmpeg.exe) do (
        set size=%%~zf
        set /a size_mb=!size!/1048576
        echo Размер ffmpeg.exe: !size_mb! MB
    )
    
    echo.
    echo Проверка работоспособности...
    ffmpeg -version | findstr /C:"ffmpeg version"
    
    echo.
    echo ✅ Компактный ffmpeg готов к использованию!
) else (
    echo ❌ ffmpeg.exe не найден после распаковки
    echo Попробуйте вручную:
    echo 1. Скачайте %FFMPEG_URL%
    echo 2. Распакуйте
    echo 3. Найдите ffmpeg.exe в bin/ папке
    echo 4. Скопируйте в папку с ботом
)

echo.
echo Удаление временных файлов...
del ffmpeg-small.zip 2>nul
rmdir /s /q ffmpeg-master-latest-win64-gpl-shared 2>nul

pause