import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import yt_dlp
import json
import os

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

# ── FFmpeg — check local folder first, then rely on PATH ──────────────────────
_FFMPEG_LOCAL = os.path.join(_HERE, 'ffmpeg.exe')
FFMPEG_EXE = _FFMPEG_LOCAL if os.path.exists(_FFMPEG_LOCAL) else 'ffmpeg'

FFMPEG_OPTIONS = {
    'executable': FFMPEG_EXE,
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

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
bot = commands.Bot(command_prefix=config.get('prefix', '/'), intents=intents)


@bot.event
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    print(f'[ERROR] /{interaction.command.name if interaction.command else "?"}: {error}')
    try:
        await interaction.response.send_message(f'❌ Error: {error}', ephemeral=True)
    except Exception:
        pass


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (id: {bot.user.id})')
    print(f'Guilds: {[g.name for g in bot.guilds]}')

    await bot.add_cog(MusicCog(bot))

    try:
        synced = await bot.tree.sync()
        print(f'Global sync OK: {len(synced)} commands')
    except Exception as e:
        print(f'Global sync FAILED: {e}')

    print('Bot ready!')


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

            source = discord.FFmpegPCMAudio(
                tmp_path,
                executable=FFMPEG_EXE
            )
            vc.play(source, after=cleanup)

            preview = text if len(text) <= 60 else text[:60] + '…'
            embed = discord.Embed(
                title='🗣️ TTS',
                description=f'`{preview}`',
                color=0xA855F7
            )
            embed.set_footer(text=f'lang: {lang}')
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f'❌ TTS error: {e}', ephemeral=True)

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
    bot.run(config['api_key'])
