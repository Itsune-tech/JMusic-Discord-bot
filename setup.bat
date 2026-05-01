@echo off
echo Setting up JMusic Discord Bot...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    echo Please check your Python installation.
    pause
    exit /b 1
)

echo.
echo Checking configuration...
if not exist "config.json" (
    echo config.json not found. Creating from example...
    copy config.example.json config.json
    echo Please edit config.json and add your Discord bot token.
) else (
    echo config.json already exists.
)

echo.
echo Setup complete!
echo.
echo To run the bot:
echo    python bot.py
echo.
echo Don't forget to:
echo 1. Add your Discord bot token to config.json
echo 2. Enable privileged intents in Discord Developer Portal
echo 3. Invite the bot to your server
echo.
pause