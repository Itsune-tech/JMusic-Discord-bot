#!/bin/bash
# Скрипт который ОБХОДИТ систему bothost.ru и устанавливает зависимости

echo "=== ОБХОД СИСТЕМЫ BOTHOST.RU ==="
echo "Проблема: bothost.ru игнорирует Build Command и устанавливает только ffmpeg-python"

# Удаляем всё что мешает
echo "1. Очищаю систему..."
rm -f requirements.txt 2>/dev/null || true

# Создаем скрипт установки который запустится при старте бота
echo "2. Создаю скрипт автоматической установки..."
cat > /app/auto_install.py << 'EOF'
#!/usr/bin/env python3
"""
Скрипт автоматической установки зависимостей при запуске бота
"""
import subprocess
import sys
import os

def install_deps():
    print("=" * 60)
    print("АВТОМАТИЧЕСКАЯ УСТАНОВКА ЗАВИСИМОСТЕЙ")
    print("=" * 60)
    
    deps = ["discord.py", "pynacl", "yt-dlp", "gtts", "ffmpeg-python"]
    
    for dep in deps:
        print(f"Устанавливаю {dep}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
            print(f"✅ {dep} установлен")
        except:
            print(f"⚠️ Не удалось установить {dep}")
    
    print("=" * 60)
    print("УСТАНОВКА ЗАВЕРШЕНА")
    print("=" * 60)

if __name__ == "__main__":
    install_deps()
EOF

# Делаем исполняемым
chmod +x /app/auto_install.py

# Создаем обертку для bot.py
echo "3. Создаю обертку для bot.py..."
cat > /app/start_bot.sh << 'EOF'
#!/bin/bash
# Обертка которая сначала установит зависимости, потом запустит бота

echo "=== ЗАПУСК DISCORD БОТА ==="

# Проверяем PyNaCl
python3 -c "import nacl" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ PyNaCl не установлен, устанавливаю..."
    python3 /app/auto_install.py
else
    echo "✅ PyNaCl уже установлен"
fi

# Запускаем бота
echo "Запускаю бота..."
exec python3 bot.py
EOF

chmod +x /app/start_bot.sh

echo "4. Меняю CMD в Dockerfile..."
# Создаем новый Dockerfile
cat > /app/Dockerfile << 'EOF'
FROM python:3.11-slim
RUN apt-get update && apt-get install -y ffmpeg
WORKDIR /app
COPY . .
CMD ["/bin/bash", "/app/start_bot.sh"]
EOF

echo "=== ГОТОВО ==="
echo "Теперь бот будет автоматически устанавливать зависимости при запуске"
echo "Даже если bothost.ru их не установил"