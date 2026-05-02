import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import yt_dlp
import json
import os
import sys

# Глобальный обработчик исключений для отладки
import traceback

def log_error(msg):
    print(f"❌ ОШИБКА: {msg}")
    traceback.print_exc()

print("=" * 60)
print("🚀 ЗАПУСК JMusic Discord Bot")
print(f"Python: {sys.version}")
print(f"Платформа: {sys.platform}")
print(f"Рабочая директория: {os.getcwd()}")
print("=" * 60)

# ── Проверка и АВТОМАТИЧЕСКАЯ установка зависимостей ───────────────────────
print("=" * 60)
print("🔍 ДИАГНОСТИКА И АВТОМАТИЧЕСКАЯ УСТАНОВКА ЗАВИСИМОСТЕЙ")
print("=" * 60)

import subprocess
import sys

# Проверяем ВСЕ критические зависимости
deps = {
    "discord": ("discord.py[voice]", "discord.py[voice]"),
    "nacl": ("PyNaCl (критически для голоса!)", "pynacl"),
    "yt_dlp": ("yt-dlp", "yt-dlp"),
    "gtts": ("gTTS", "gtts"),
    "ffmpeg": ("ffmpeg-python", "ffmpeg-python"),
    "dotenv": ("python-dotenv", "python-dotenv")
}

missing_deps = []
for import_name, (package_name, pip_name) in deps.items():
    try:
        if import_name == "ffmpeg":
            import ffmpeg
        else:
            __import__(import_name)
        print(f"✅ {package_name} установлен")
    except ImportError:
        print(f"❌ {package_name} НЕ УСТАНОВЛЕН!")
        missing_deps.append(pip_name)
        if import_name == "nacl":
            print("   ⚠️ БЕЗ PyNaCl ГОЛОСОВОЙ ФУНКЦИОНАЛ НЕ РАБОТАЕТ!")

print("=" * 60)

# АВТОМАТИЧЕСКАЯ УСТАНОВКА если чего-то не хватает
if missing_deps:
    print(f"⚠️ Отсутствуют {len(missing_deps)} зависимостей")
    print("Пробую установить автоматически...")
    
    for dep in missing_deps:
        print(f"Устанавливаю {dep}...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", dep],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"✅ {dep} установлен")
            else:
                print(f"❌ Не удалось установить {dep}: {result.stderr[:100]}")
        except Exception as e:
            print(f"❌ Ошибка установки {dep}: {e}")
    
    # Проверяем снова после установки
    print("\n🔍 Проверяю установку после автоматической инсталляции...")
    for import_name, (package_name, _) in deps.items():
        try:
            if import_name == "ffmpeg":
                import ffmpeg
            else:
                __import__(import_name)
            print(f"✅ {package_name} теперь установлен")
        except ImportError:
            print(f"❌ {package_name} всё ещё не установлен")

print("=" * 60)
print("✅ ДИАГНОСТИКА ЗАВЕРШЕНА")
print("=" * 60)

# Дополнительная проверка голосовых зависимостей
print("🔊 Проверка голосовых зависимостей...")
try:
    import nacl
    print("✅ PyNaCl установлен и готов к работе с голосом")
except ImportError:
    print("❌ PyNaCl не установлен! Голосовой функционал не будет работать!")
    print("   Установите: pip install pynacl")

# Проверка Opus библиотеки
try:
    import discord.opus
    if discord.opus.is_loaded():
        print("✅ Библиотека Opus загружена (для голосового чата)")
    else:
        print("⚠️ Библиотека Opus не загружена, попробую загрузить...")
        try:
            discord.opus.load_opus('libopus.so.0')
            if discord.opus.is_loaded():
                print("✅ Библиотека Opus успешно загружена")
            else:
                print("❌ Не удалось загрузить библиотеку Opus")
                print("   В Docker: установите libopus-dev")
        except Exception as e:
            print(f"❌ Ошибка загрузки Opus: {e}")
except Exception as e:
    print(f"⚠️ Не удалось проверить Opus: {e}")
    
print("=" * 60)

# ── Config ────────────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH     = os.path.join(_HERE, 'config.json')
PLAYLISTS_PATH  = os.path.join(_HERE, 'playlists.json')

# Try to get token from environment variable first (for production)
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

if DISCORD_TOKEN:
    # Use environment variable
    config = {'api_key': DISCORD_TOKEN, 'prefix': '/'}
else:
    # Fall back to config file (for development)
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Config file not found at {CONFIG_PATH}")
        print("Please create config.json or set DISCORD_TOKEN environment variable")
        exit(1)

# ── FFmpeg — ищем в той же папке что и бот, затем в системе ──────────────────
# Все пути относительно расположения файла бота
_FFMPEG_LOCAL_WIN = os.path.join(_HERE, 'ffmpeg.exe')
_FFMPEG_LOCAL_LINUX = os.path.join(_HERE, 'ffmpeg')  # Linux бинарник без расширения

# Также проверяем в подпапках (на всякий случай)
_FFMPEG_IN_SAME_DIR_WIN = os.path.join(_HERE, 'ffmpeg.exe')
_FFMPEG_IN_SAME_DIR_LINUX = os.path.join(_HERE, 'ffmpeg')

# Системные пути (стандартные для Linux)
_FFMPEG_LINUX = '/usr/bin/ffmpeg'
_FFMPEG_LINUX_LOCAL = '/usr/local/bin/ffmpeg'

# Специальные пути для bothost.ru (если ffmpeg предустановлен)
_FFMPEG_BOTHOST_1 = '/usr/local/bin/ffmpeg'
_FFMPEG_BOTHOST_2 = '/usr/bin/ffmpeg'
_FFMPEG_BOTHOST_3 = '/opt/ffmpeg/bin/ffmpeg'

print(f"📁 Текущая директория бота: {_HERE}")
print(f"🔍 Ищу ffmpeg в: {_FFMPEG_LOCAL_LINUX}")

# Принудительно выводим список файлов в директории для отладки
try:
    files = os.listdir(_HERE)
    print(f"📂 Файлы в директории бота: {', '.join(files[:10])}" + ("..." if len(files) > 10 else ""))
except Exception as e:
    print(f"⚠️ Не удалось прочитать директорию: {e}")

FFMPEG_EXE = 'ffmpeg'  # По умолчанию используем системный (через PATH)

# Определяем, работаем ли мы в Docker/Linux окружении
IS_DOCKER = os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv')
IS_LINUX = sys.platform.startswith('linux')

print(f"🔧 Окружение: {'Docker' if IS_DOCKER else 'Не Docker'}, {'Linux' if IS_LINUX else 'Не Linux'}")

# ПРОСТАЯ И НАДЕЖНАЯ ЛОГИКА для Docker
ffmpeg_paths = []

if IS_DOCKER:
    # В DOCKER: ПРОСТОЙ И НАДЕЖНЫЙ ПОИСК
    print("🐳 В Docker: использую простую логику поиска ffmpeg")
    
    # 1. Сначала пробуем команду 'ffmpeg' (через PATH) - самый надежный способ
    #    если ffmpeg установлен через apt-get, он будет в PATH
    ffmpeg_paths.append(('ffmpeg', "Команда 'ffmpeg' через PATH"))
    
    # 2. Проверяем стандартные пути где обычно находится ffmpeg
    standard_paths = [
        '/usr/bin/ffmpeg',
        '/usr/local/bin/ffmpeg',
        '/bin/ffmpeg',
        '/app/ffmpeg',  # Локальный (последний выбор, обычно не работает)
    ]
    
    for path in standard_paths:
        ffmpeg_paths.append((path, f"Файл {path}"))
    
    print(f"   Буду проверять: {', '.join([p[0] for p in ffmpeg_paths])}")
    
elif IS_LINUX:
    # В Linux (не Docker)
    ffmpeg_paths = [
        ('ffmpeg', "Команда 'ffmpeg' через PATH"),
        '/usr/bin/ffmpeg',
        '/usr/local/bin/ffmpeg',
        '/bin/ffmpeg',
        _FFMPEG_LOCAL_LINUX,  # Локальный в папке бота
    ]
    # Преобразуем в формат (путь, описание)
    ffmpeg_paths = [(p if isinstance(p, str) else p[0], 
                     p[1] if isinstance(p, tuple) else f"Файл {p}") 
                    for p in ffmpeg_paths]
else:
    # В Windows
    ffmpeg_paths = [
        (_FFMPEG_LOCAL_WIN, "Локальный Windows ffmpeg.exe"),
        ('ffmpeg', "Команда 'ffmpeg' через PATH"),
    ]

print(f"🔍 Буду проверять {len(ffmpeg_paths)} путей к ffmpeg")

# Проверяем все возможные пути с проверкой работоспособности
ffmpeg_found = False
working_ffmpeg = None
working_description = None

for path, description in ffmpeg_paths:
    print(f"🔍 Проверяю {description}: {path}")
    
    # Для команды 'ffmpeg' (через PATH) не проверяем os.path.exists
    # Для файловых путей проверяем существование
    if path != 'ffmpeg' and not os.path.exists(path):
        print(f"  ⚠️ Файл не существует, пропускаю...")
        continue
    
    # Для Linux файлов проверяем и устанавливаем права на выполнение
    if path != 'ffmpeg' and (IS_LINUX or IS_DOCKER):
        try:
            import stat
            # Проверяем права доступа
            st = os.stat(path)
            if not (st.st_mode & stat.S_IEXEC):
                print(f"  ⚠️ Файл не имеет прав на выполнение, устанавливаю...")
                try:
                    os.chmod(path, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
                    print(f"  ✅ Права на выполнение установлены")
                except Exception as e:
                    print(f"  ⚠️ Не удалось установить права: {e}")
        except Exception as e:
            print(f"  ⚠️ Не удалось проверить права файла: {e}")
    
    # Проверяем, что ffmpeg действительно работает
    try:
        import subprocess
        print(f"  🧪 Запускаю: {path} -version")
        result = subprocess.run([path, '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"  ✅ FFmpeg работает: {version_line}")
            working_ffmpeg = path
            working_description = description
            ffmpeg_found = True
            break
        else:
            error_msg = result.stderr[:200] if result.stderr else "неизвестная ошибка"
            stdout_msg = result.stdout[:100] if result.stdout else "нет вывода"
            print(f"  ⚠️ FFmpeg не работает. stderr: {error_msg}")
            print(f"     stdout: {stdout_msg}")
            
            # В Docker: если это локальный файл с ошибкой библиотек - пропускаем сразу
            if IS_DOCKER and path == '/app/ffmpeg' and ("libavdevice.so" in error_msg or "cannot open shared object file" in error_msg):
                print(f"  ⚠️ В Docker: локальный /app/ffmpeg не работает (библиотеки), пропускаю")
                continue
            
            # Общие проверки ошибок библиотек
            skip_keywords = ["libavdevice.so", "cannot open shared object file", "libav", "not a win32", "не является приложением win32"]
            if any(keyword.lower() in error_msg.lower() for keyword in skip_keywords):
                print(f"  ⚠️ Пропускаю из-за ошибки библиотек/совместимости")
                continue
            
    except Exception as e:
        error_str = str(e)
        print(f"  ⚠️ Не удалось запустить ffmpeg: {error_str}")
        
        # В Docker: если это локальный файл с ошибкой - пропускаем
        if IS_DOCKER and path == '/app/ffmpeg' and ("libavdevice" in error_str or "shared object" in error_str):
            print(f"  ⚠️ В Docker: локальный /app/ffmpeg не работает, пропускаю")
            continue
        
        # Общие проверки ошибок библиотек
        if "libavdevice" in error_str or "shared object" in error_str:
            print(f"  ⚠️ Пропускаю из-за ошибки библиотек")
            continue

# Устанавливаем рабочий ffmpeg
if working_ffmpeg:
    FFMPEG_EXE = working_ffmpeg
    print(f"✓ Использую {working_description}: {working_ffmpeg}")
    ffmpeg_found = True
else:
    # Не нашли работающий ffmpeg
    print("⚠️ Рабочий ffmpeg не найден после проверки всех путей")
    
    # В Docker: ПРОСТО ИСПОЛЬЗУЕМ 'ffmpeg' (через PATH)
    if IS_DOCKER:
        print("🐳 В Docker: использую 'ffmpeg' через PATH (самый надежный способ)")
        FFMPEG_EXE = 'ffmpeg'
        
        # Проверяем работает ли
        import subprocess
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"✅ 'ffmpeg' работает: {version_line}")
                ffmpeg_found = True
            else:
                error_msg = result.stderr[:200] if result.stderr else "нет вывода"
                print(f"❌ 'ffmpeg' не работает: {error_msg}")
                print("   Убедитесь что в Dockerfile есть: RUN apt-get install -y ffmpeg")
        except Exception as e:
            print(f"❌ Не удалось запустить 'ffmpeg': {e}")
    else:
        # Не Docker: последняя попытка
        FFMPEG_EXE = 'ffmpeg'
        print(f"🔄 Последняя попытка: использую 'ffmpeg' через PATH")
        
        import subprocess
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"✓ 'ffmpeg' через PATH работает: {version_line}")
                ffmpeg_found = True
            else:
                error_msg = result.stderr[:200] if result.stderr else "нет вывода"
                print(f"❌ 'ffmpeg' через PATH не работает: {error_msg}")
        except Exception as e:
            print(f"❌ Не удалось запустить 'ffmpeg': {e}")
    
    if not ffmpeg_found:
        print("❌ FFmpeg не найден или не работает!")
        print("   В Docker: убедитесь что в Dockerfile есть:")
        print("     RUN apt-get update && apt-get install -y ffmpeg")
        print("   И пересоберите контейнер")

# Check if FFmpeg is available
def check_ffmpeg():
    import subprocess
    try:
        # Try to run ffmpeg -version
        result = subprocess.run([FFMPEG_EXE, '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✓ FFmpeg доступен: {version_line}")
            return True
        else:
            error_msg = result.stderr[:200] if result.stderr else "нет вывода"
            print(f"✗ FFmpeg вернул ошибку: {error_msg}")
            print(f"  Путь: {FFMPEG_EXE}")
            return False
    except (subprocess.SubprocessError, FileNotFoundError, OSError) as e:
        print(f"✗ Не удалось запустить ffmpeg: {e}")
        print(f"  Искал по пути: {FFMPEG_EXE}")
        print("  В Docker: убедитесь что 'apt-get install ffmpeg' выполнен")
        print("  Ссылка: https://ffmpeg.org/download.html")
        return False

# Проверяем ffmpeg при запуске
print("=" * 60)
print("🔧 ПРОВЕРКА FFMPEG")
print("=" * 60)
ffmpeg_available = check_ffmpeg()
if not ffmpeg_available:
    print("❌ FFmpeg не найден! Бот не сможет воспроизводить музыку.")
    print("   Установите ffmpeg или убедитесь, что он есть в PATH.")
else:
    print("✅ FFmpeg готов к работе!")
print("=" * 60)

# Создаем безопасные FFMPEG_OPTIONS
# Если FFMPEG_EXE это просто 'ffmpeg' (команда в PATH), не проверяем os.path.exists
safe_ffmpeg_exe = FFMPEG_EXE
if safe_ffmpeg_exe != 'ffmpeg' and not os.path.exists(safe_ffmpeg_exe):
    print(f"⚠️ FFMPEG_EXE не существует как файл: {safe_ffmpeg_exe}, использую 'ffmpeg'")
    safe_ffmpeg_exe = 'ffmpeg'

FFMPEG_OPTIONS = {
    'executable': safe_ffmpeg_exe,
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

print(f"🔧 FFMPEG_OPTIONS использует: {safe_ffmpeg_exe}")

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'default_search': 'ytsearch',   # fallback: search YouTube by keywords
    'source_address': '0.0.0.0',
}

# ── Per-guild queue ────────────────────────────────────────────────────────────
# { guild_id: {'queue': [...], 'current': None} }
guild_state: dict = {}

def get_state(guild_id: int) -> dict:
    if guild_id not in guild_state:
        guild_state[guild_id] = {'queue': [], 'current': None}
    return guild_state[guild_id]


# ── Playlist persistence ───────────────────────────────────────────────────────
# Structure: { "guild_id": { "playlist_name": [ {"title": ..., "webpage": ...}, ... ] } }

def _load_playlists() -> dict:
    if not os.path.exists(PLAYLISTS_PATH):
        return {}
    with open(PLAYLISTS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def _save_playlists(data: dict) -> None:
    with open(PLAYLISTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _guild_playlists(guild_id: int) -> dict:
    """Return the playlists dict for a guild (live reference after load)."""
    data = _load_playlists()
    return data.get(str(guild_id), {})


def resolve_track(query: str) -> dict | None:
    """Return track info dict or None on failure."""
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
            # If it's a search result, take the first entry
            if 'entries' in info:
                info = info['entries'][0]
            return {
                'url':      info['url'],
                'title':    info.get('title', 'Unknown'),
                'webpage':  info.get('webpage_url', ''),
                'duration': info.get('duration', 0),
            }
        except Exception as e:
            print(f'[yt-dlp] {e}')
            return None


# ── Bot setup ─────────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True

# Пытаемся загрузить Opus библиотеку перед созданием бота
try:
    import discord.opus
    if not discord.opus.is_loaded():
        print("🔊 Пытаюсь загрузить библиотеку Opus...")
        # Пробуем разные пути к библиотеке Opus
        opus_paths = ['libopus.so.0', 'libopus.so', '/usr/lib/x86_64-linux-gnu/libopus.so.0']
        for path in opus_paths:
            try:
                discord.opus.load_opus(path)
                if discord.opus.is_loaded():
                    print(f"✅ Opus загружен из {path}")
                    break
            except Exception:
                continue
        
        if not discord.opus.is_loaded():
            print("⚠️ Не удалось загрузить Opus, но продолжаю работу")
except Exception as e:
    print(f"⚠️ Ошибка загрузки Opus: {e}")

bot = commands.Bot(command_prefix=config.get('prefix', '/'), intents=intents)

# Флаг готовности бота
bot.is_ready = False


@bot.event
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    print(f'[ERROR] /{interaction.command.name if interaction.command else "?"}: {error}')
    
    # Специальная обработка для CommandNotFound
    if isinstance(error, app_commands.errors.CommandNotFound):
        if not hasattr(bot, 'is_ready') or not bot.is_ready:
            try:
                await interaction.response.send_message(
                    '⚠️ Бот еще не полностью загрузился. Подождите несколько секунд...',
                    ephemeral=True
                )
                return
            except Exception:
                pass
    
    try:
        await interaction.response.send_message(f'❌ Error: {error}', ephemeral=True)
    except Exception:
        pass


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (id: {bot.user.id})')
    print(f'Guilds: {[g.name for g in bot.guilds]}')

    # Add the cog first
    await bot.add_cog(MusicCog(bot))
    
    # Wait a moment to ensure all commands are registered
    await asyncio.sleep(1)
    
    # Sync commands globally
    try:
        synced = await bot.tree.sync()
        print(f'✅ Global sync OK: {len(synced)} commands synced')
        # List all synced commands
        for cmd in synced:
            print(f'   - /{cmd.name}')
    except Exception as e:
        print(f'❌ Global sync FAILED: {e}')
        # Try to sync to specific guilds as fallback
        try:
            for guild in bot.guilds:
                synced = await bot.tree.sync(guild=guild)
                print(f'✅ Guild sync OK for {guild.name}: {len(synced)} commands')
        except Exception as e2:
            print(f'❌ Guild sync also failed: {e2}')

    # Устанавливаем флаг готовности
    bot.is_ready = True
    print('✅ Bot ready!')


# ── Music Cog ─────────────────────────────────────────────────────────────────
class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ── helpers ───────────────────────────────────────────────────────────────

    async def _ensure_voice(self, interaction: discord.Interaction) -> discord.VoiceClient | None:
        """Join the user's voice channel, or return existing VC. Returns None if user not in VC."""
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message(
                '❌ Сначала зайди в голосовой канал.', ephemeral=True
            )
            return None

        channel = interaction.user.voice.channel
        vc: discord.VoiceClient | None = interaction.guild.voice_client

        if vc is None:
            vc = await channel.connect()
        elif vc.channel != channel:
            await vc.move_to(channel)

        return vc

    def _play_next(self, guild_id: int, vc: discord.VoiceClient):
        """Called when a track finishes — plays next in queue."""
        state = get_state(guild_id)
        if state['queue']:
            track = state['queue'].pop(0)
            state['current'] = track
            source = discord.FFmpegPCMAudio(track['url'], **FFMPEG_OPTIONS)
            vc.play(source, after=lambda e: self._play_next(guild_id, vc))
        else:
            state['current'] = None

    # ── /play ─────────────────────────────────────────────────────────────────

    @app_commands.command(name='play', description='Play music by keywords or URL')
    @app_commands.describe(query='Keywords or YouTube / streaming URL')
    async def play(self, interaction: discord.Interaction, query: str):
        vc = await self._ensure_voice(interaction)
        if vc is None:
            return

        await interaction.response.defer(thinking=True)

        track = await asyncio.get_event_loop().run_in_executor(None, resolve_track, query)
        if track is None:
            await interaction.followup.send('❌ Не удалось найти трек.', ephemeral=True)
            return

        state = get_state(interaction.guild_id)

        if vc.is_playing() or vc.is_paused():
            # Add to queue
            state['queue'].append(track)
            mins, secs = divmod(track['duration'], 60)
            embed = discord.Embed(
                title='🎵 Добавлено в очередь',
                description=f"[{track['title']}]({track['webpage']})",
                color=0xA855F7
            )
            embed.set_footer(text=f"Длительность: {mins}:{secs:02d} • Позиция: #{len(state['queue'])}")
            await interaction.followup.send(embed=embed)
        else:
            # Play immediately
            state['current'] = track
            source = discord.FFmpegPCMAudio(track['url'], **FFMPEG_OPTIONS)
            vc.play(source, after=lambda e: self._play_next(interaction.guild_id, vc))
            mins, secs = divmod(track['duration'], 60)
            embed = discord.Embed(
                title='▶️ Сейчас играет',
                description=f"[{track['title']}]({track['webpage']})",
                color=0xA855F7
            )
            embed.set_footer(text=f"Длительность: {mins}:{secs:02d}")
            await interaction.followup.send(embed=embed)

    # ── /pause ────────────────────────────────────────────────────────────────

    @app_commands.command(name='pause', description='Pause playback')
    async def pause(self, interaction: discord.Interaction):
        vc: discord.VoiceClient | None = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await interaction.response.send_message('⏸️ Пауза.', ephemeral=True)
        else:
            await interaction.response.send_message('❌ Ничего не играет.', ephemeral=True)

    # ── /unpause ──────────────────────────────────────────────────────────────

    @app_commands.command(name='unpause', description='Resume playback')
    async def unpause(self, interaction: discord.Interaction):
        vc: discord.VoiceClient | None = interaction.guild.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await interaction.response.send_message('▶️ Продолжаю.', ephemeral=True)
        else:
            await interaction.response.send_message('❌ Плеер не на паузе.', ephemeral=True)

    # ── /stop ─────────────────────────────────────────────────────────────────

    @app_commands.command(name='stop', description='Stop and leave voice channel')
    async def stop(self, interaction: discord.Interaction):
        vc: discord.VoiceClient | None = interaction.guild.voice_client
        if vc:
            state = get_state(interaction.guild_id)
            state['queue'].clear()
            state['current'] = None
            await vc.disconnect()
            await interaction.response.send_message('⏹️ Остановлено, вышел из канала.', ephemeral=True)
        else:
            await interaction.response.send_message('❌ Бот не в голосовом канале.', ephemeral=True)

    # ── /queue ────────────────────────────────────────────────────────────────

    @app_commands.command(name='queue', description='Show current queue')
    async def queue(self, interaction: discord.Interaction):
        state = get_state(interaction.guild_id)
        current = state.get('current')
        queue   = state.get('queue', [])

        if not current and not queue:
            await interaction.response.send_message('📭 Очередь пуста.', ephemeral=True)
            return

        embed = discord.Embed(title='🎶 Очередь', color=0xA855F7)

        if current:
            embed.add_field(
                name='▶️ Сейчас',
                value=f"[{current['title']}]({current['webpage']})",
                inline=False
            )

        if queue:
            lines = [f"`{i+1}.` [{t['title']}]({t['webpage']})" for i, t in enumerate(queue[:10])]
            if len(queue) > 10:
                lines.append(f'_...и ещё {len(queue) - 10}_')
            embed.add_field(name='📋 Далее', value='\n'.join(lines), inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    # ── /skip ─────────────────────────────────────────────────────────────────

    @app_commands.command(name='skip', description='Skip current track')
    async def skip(self, interaction: discord.Interaction):
        vc: discord.VoiceClient | None = interaction.guild.voice_client
        if vc and (vc.is_playing() or vc.is_paused()):
            vc.stop()
            await interaction.response.send_message('⏭️ Пропущено.', ephemeral=True)
        else:
            await interaction.response.send_message('❌ Ничего не играет.', ephemeral=True)

    # ── /tts ──────────────────────────────────────────────────────────────────

    @app_commands.command(name='tts', description='Say text in voice channel')
    @app_commands.describe(
        text='Text to speak',
        lang='Language code (default: ru). Examples: en, ru, de, fr, ja'
    )
    async def tts(self, interaction: discord.Interaction, text: str, lang: str = 'ru'):
        vc = await self._ensure_voice(interaction)
        if vc is None:
            return

        await interaction.response.defer(thinking=True)

        try:
            from gtts import gTTS
            import tempfile

            tts_obj = gTTS(text=text, lang=lang)
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                tmp_path = f.name
            tts_obj.save(tmp_path)

            # If something is playing, wait; otherwise play immediately
            if vc.is_playing() or vc.is_paused():
                await interaction.followup.send(
                    '⚠️ Подожди пока закончится текущий трек.', ephemeral=True
                )
                return

            def cleanup(e):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

            # Для TTS используем специальные настройки FFmpeg
            # Используем FFMPEG_EXE, который уже должен быть правильным путем
            tts_ffmpeg_exe = FFMPEG_EXE
            
            # Если FFMPEG_EXE это просто 'ffmpeg' (команда в PATH), не проверяем os.path.exists
            # потому что os.path.exists('ffmpeg') вернет False для команд в PATH
            if tts_ffmpeg_exe != 'ffmpeg' and not os.path.exists(tts_ffmpeg_exe):
                print(f"⚠️ FFMPEG_EXE не существует как файл: {tts_ffmpeg_exe}, использую 'ffmpeg'")
                tts_ffmpeg_exe = 'ffmpeg'
            
            tts_ffmpeg_options = {
                'executable': tts_ffmpeg_exe,
                'options': '-vn'
            }
            
            source = discord.FFmpegPCMAudio(tmp_path, **tts_ffmpeg_options)
            vc.play(source, after=cleanup)

            preview = text if len(text) <= 60 else text[:60] + '…'
            embed = discord.Embed(
                title='🗣️ TTS',
                description=f'`{preview}`',
                color=0xA855F7
            )
            embed.set_footer(text=f'lang: {lang}')
            await interaction.followup.send(embed=embed)

        except discord.opus.OpusNotLoaded as e:
            print(f"[TTS ERROR] OpusNotLoaded: {e}")
            error_msg = f"❌ Библиотека Opus не загружена!\n"
            error_msg += f"Без Opus голосовой чат Discord не работает.\n"
            error_msg += f"В Docker: убедитесь что 'libopus-dev' установлен\n"
            error_msg += f"Проверьте Dockerfile и пересоберите контейнер"
            await interaction.followup.send(error_msg, ephemeral=True)
        except Exception as e:
            print(f"[TTS ERROR] {e}")
            error_msg = str(e)
            # Более информативные сообщения об ошибках ffmpeg
            if "ffmpeg" in error_msg.lower() or "file not found" in error_msg.lower() or "not found" in error_msg.lower():
                error_msg = f"❌ FFmpeg не найден или не работает.\n"
                error_msg += f"Проверьте что ffmpeg установлен в системе.\n"
                error_msg += f"В Docker: `apt-get install ffmpeg`\n"
                error_msg += f"Текущий путь: `{tts_ffmpeg_exe}`"
            elif "libavdevice.so" in error_msg.lower() or "shared object file" in error_msg.lower():
                error_msg = f"❌ Проблема с библиотеками ffmpeg.\n"
                error_msg += f"Локальный ffmpeg требует библиотек которых нет.\n"
                error_msg += f"Используйте системный ffmpeg (установленный через apt-get)"
            
            # Убедимся что сообщение не пустое
            if not error_msg or error_msg.strip() == "":
                error_msg = f"❌ Неизвестная ошибка TTS: {type(e).__name__}"
            
            await interaction.followup.send(error_msg, ephemeral=True)

    # ── /playlist ─────────────────────────────────────────────────────────────
    #
    #  Subcommands (action):
    #    list              — show all playlists in this guild
    #    list  <name>      — show songs inside a playlist
    #    add   <query> <name> — resolve track and add to playlist (creates if needed)
    #    play  <name>      — queue all songs from a playlist
    #    delete <name>     — delete an entire playlist
    #    remove <name> <index> — remove one song by its 0-based index shown in list
    #    import <url>      — import a YouTube playlist by URL
    # ──────────────────────────────────────────────────────────────────────────

    playlist_group = app_commands.Group(name='playlist', description='Manage saved playlists')

    @playlist_group.command(name='list', description='List all playlists, or songs inside one')
    @app_commands.describe(name='Playlist name (leave empty to list all playlists)')
    async def playlist_list(self, interaction: discord.Interaction, name: str = ''):
        playlists = _guild_playlists(interaction.guild_id)

        if not name:
            # Show all playlists
            if not playlists:
                await interaction.response.send_message('📭 Нет сохранённых плейлистов.', ephemeral=True)
                return
            lines = [f'`[{i}]` {pl_name} — {len(songs)} трек(ов)'
                     for i, (pl_name, songs) in enumerate(playlists.items())]
            embed = discord.Embed(title='📋 Плейлисты', description='\n'.join(lines), color=0xA855F7)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            # Show songs in a specific playlist
            if name not in playlists:
                await interaction.response.send_message(f'❌ Плейлист `{name}` не найден.', ephemeral=True)
                return
            songs = playlists[name]
            if not songs:
                await interaction.response.send_message(f'📭 Плейлист `{name}` пуст.', ephemeral=True)
                return
            lines = [f'`[{i}]` [{s["title"]}]({s["webpage"]})' for i, s in enumerate(songs)]
            embed = discord.Embed(
                title=f'🎵 {name}',
                description='\n'.join(lines[:20]) + (f'\n_...и ещё {len(lines)-20}_' if len(lines) > 20 else ''),
                color=0xA855F7
            )
            embed.set_footer(text=f'{len(songs)} трек(ов)')
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @playlist_group.command(name='add', description='Add a song to a playlist (creates playlist if needed)')
    @app_commands.describe(
        query='Keywords or YouTube URL',
        name='Playlist name'
    )
    async def playlist_add(self, interaction: discord.Interaction, query: str, name: str):
        await interaction.response.defer(thinking=True, ephemeral=True)

        track = await asyncio.get_event_loop().run_in_executor(None, resolve_track, query)
        if track is None:
            await interaction.followup.send('❌ Не удалось найти трек.', ephemeral=True)
            return

        data = _load_playlists()
        gid  = str(interaction.guild_id)
        data.setdefault(gid, {}).setdefault(name, [])
        data[gid][name].append({'title': track['title'], 'webpage': track['webpage']})
        _save_playlists(data)

        embed = discord.Embed(
            title='✅ Добавлено в плейлист',
            description=f"[{track['title']}]({track['webpage']})\n→ плейлист **{name}**",
            color=0xA855F7
        )
        embed.set_footer(text=f'Треков в плейлисте: {len(data[gid][name])}')
        await interaction.followup.send(embed=embed, ephemeral=True)

    @playlist_group.command(name='play', description='Queue all songs from a playlist')
    @app_commands.describe(name='Playlist name')
    async def playlist_play(self, interaction: discord.Interaction, name: str):
        playlists = _guild_playlists(interaction.guild_id)
        if name not in playlists:
            await interaction.response.send_message(f'❌ Плейлист `{name}` не найден.', ephemeral=True)
            return
        songs = playlists[name]
        if not songs:
            await interaction.response.send_message(f'📭 Плейлист `{name}` пуст.', ephemeral=True)
            return

        vc = await self._ensure_voice(interaction)
        if vc is None:
            return

        await interaction.response.defer(thinking=True)

        # Resolve all tracks concurrently
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(None, resolve_track, s['webpage'] or s['title']) for s in songs]
        resolved = await asyncio.gather(*tasks)

        state   = get_state(interaction.guild_id)
        added   = 0
        failed  = 0
        for track in resolved:
            if track:
                state['queue'].append(track)
                added += 1
            else:
                failed += 1

        # Start playback if nothing is playing
        if not vc.is_playing() and not vc.is_paused() and state['queue']:
            track = state['queue'].pop(0)
            state['current'] = track
            source = discord.FFmpegPCMAudio(track['url'], **FFMPEG_OPTIONS)
            vc.play(source, after=lambda e: self._play_next(interaction.guild_id, vc))

        embed = discord.Embed(
            title=f'▶️ Плейлист: {name}',
            description=f'Добавлено в очередь: **{added}** трек(ов)' +
                        (f'\n⚠️ Не удалось загрузить: {failed}' if failed else ''),
            color=0xA855F7
        )
        await interaction.followup.send(embed=embed)

    @playlist_group.command(name='delete', description='Delete an entire playlist by its index')
    @app_commands.describe(index='Playlist index (number shown in /playlist list)')
    async def playlist_delete(self, interaction: discord.Interaction, index: int):
        data = _load_playlists()
        gid  = str(interaction.guild_id)
        playlists = data.get(gid, {})
        if not playlists:
            await interaction.response.send_message('📭 Нет сохранённых плейлистов.', ephemeral=True)
            return
        names = list(playlists.keys())
        if index < 0 or index >= len(names):
            await interaction.response.send_message(
                f'❌ Индекс вне диапазона. Плейлистов: {len(names)} (0–{len(names)-1}).',
                ephemeral=True
            )
            return
        name = names[index]
        del data[gid][name]
        _save_playlists(data)
        await interaction.response.send_message(f'🗑️ Плейлист **{name}** удалён.', ephemeral=True)

    @playlist_group.command(name='remove', description='Remove a song from a playlist by its index')
    @app_commands.describe(
        name='Playlist name',
        index='Song index (number shown in /playlist list <name>)'
    )
    async def playlist_remove(self, interaction: discord.Interaction, name: str, index: int):
        data = _load_playlists()
        gid  = str(interaction.guild_id)
        if gid not in data or name not in data[gid]:
            await interaction.response.send_message(f'❌ Плейлист `{name}` не найден.', ephemeral=True)
            return
        songs = data[gid][name]
        if index < 0 or index >= len(songs):
            await interaction.response.send_message(
                f'❌ Индекс вне диапазона. Плейлист содержит {len(songs)} трек(ов) (0–{len(songs)-1}).',
                ephemeral=True
            )
            return
        removed = songs.pop(index)
        _save_playlists(data)
        await interaction.response.send_message(
            f'🗑️ Удалено из **{name}**: [{removed["title"]}]({removed["webpage"]})',
            ephemeral=True
        )

    @playlist_group.command(name='import', description='Import a YouTube playlist by URL')
    @app_commands.describe(url='YouTube playlist URL')
    async def playlist_import(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer(thinking=True, ephemeral=True)

        def _fetch_playlist(url: str):
            opts = {
                'extract_flat': 'in_playlist',  # don't resolve each video fully
                'quiet': True,
                'noplaylist': False,
                'source_address': '0.0.0.0',
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
            return info

        try:
            info = await asyncio.get_event_loop().run_in_executor(None, _fetch_playlist, url)
        except Exception as e:
            await interaction.followup.send(f'❌ Не удалось загрузить плейлист: {e}', ephemeral=True)
            return

        if not info or 'entries' not in info:
            await interaction.followup.send('❌ Ссылка не является плейлистом или плейлист пуст.', ephemeral=True)
            return

        pl_name = info.get('title') or info.get('id') or 'Imported Playlist'
        entries = info['entries']

        songs = []
        for entry in entries:
            if not entry:
                continue
            title   = entry.get('title') or entry.get('id') or 'Unknown'
            webpage = entry.get('url') or entry.get('webpage_url') or ''
            # flat extraction gives watch URLs as 'url' field
            if webpage and not webpage.startswith('http'):
                webpage = f"https://www.youtube.com/watch?v={entry.get('id', '')}"
            songs.append({'title': title, 'webpage': webpage})

        if not songs:
            await interaction.followup.send('❌ В плейлисте не найдено треков.', ephemeral=True)
            return

        data = _load_playlists()
        gid  = str(interaction.guild_id)
        data.setdefault(gid, {})[pl_name] = songs
        _save_playlists(data)

        embed = discord.Embed(
            title='📥 Плейлист импортирован',
            description=f'**{pl_name}**\nИмпортировано треков: **{len(songs)}**',
            color=0xA855F7
        )
        embed.set_footer(text='Используй /playlist play для воспроизведения')
        await interaction.followup.send(embed=embed, ephemeral=True)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 60)
    print("🎯 ЗАПУСКАЮ БОТА")
    print("=" * 60)
    try:
        bot.run(config['api_key'])
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА ПРИ ЗАПУСКЕ БОТА: {e}")
        traceback.print_exc()
        raise
