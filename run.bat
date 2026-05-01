@echo off
echo Starting JMusic Discord Bot...
echo.

REM Check if config exists
if not exist "config.json" (
    echo config.json not found!
    echo Please copy config.example.json to config.json and add your token.
    pause
    exit /b 1
)

REM Check if token is still the example
findstr /C:"YOUR_DISCORD_BOT_TOKEN_HERE" config.json >nul
if not errorlevel 1 (
    echo Please update config.json with your actual Discord bot token.
    pause
    exit /b 1
)

echo Starting bot...
python bot.py
if errorlevel 1 (
    echo Failed to start bot.
    echo Check your configuration and dependencies.
    pause
    exit /b 1
)

pause