# JMusic Discord Bot

A feature-rich Discord music bot with playlist management, text-to-speech, and YouTube integration.

## Features

- 🎵 **Music Playback**: Play music from YouTube and other streaming services
- 📋 **Queue Management**: Add, skip, pause, and manage playback queue
- 📁 **Playlist System**: Create, save, and manage playlists
- 🗣️ **Text-to-Speech**: Convert text to speech in voice channels
- 🔄 **YouTube Integration**: Import YouTube playlists by URL
- 🎚️ **Voice Control**: Join, move between, and leave voice channels

## Commands

### Music Commands
- `/play <query>` - Play music by keywords or URL
- `/pause` - Pause playback
- `/unpause` - Resume playback
- `/stop` - Stop and leave voice channel
- `/queue` - Show current queue
- `/skip` - Skip current track

### Playlist Commands
- `/playlist list [name]` - List all playlists or songs in a playlist
- `/playlist add <query> <name>` - Add song to playlist
- `/playlist play <name>` - Queue all songs from a playlist
- `/playlist delete <index>` - Delete a playlist by index
- `/playlist remove <name> <index>` - Remove song from playlist
- `/playlist import <url>` - Import YouTube playlist by URL

### TTS Command
- `/tts <text> [lang]` - Convert text to speech (default: ru)

## Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg (included in repository)
- Discord Bot Token

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/username/jmusic-bot.git
   cd jmusic-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot:**
   - Copy `config.example.json` to `config.json`
   - Add your Discord bot token:
     ```json
     {
         "api_key": "YOUR_DISCORD_BOT_TOKEN_HERE",
         "prefix": "/"
     }
     ```

4. **Run the bot:**
   ```bash
   python bot.py
   ```

## Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section
4. Click "Add Bot"
5. Copy the bot token
6. Enable these privileged intents:
   - Presence Intent
   - Server Members Intent
   - Message Content Intent
7. Invite the bot to your server using OAuth2 URL Generator with `applications.commands` and `bot` scopes

## Configuration

The bot uses `config.json` for configuration:
```json
{
    "api_key": "your-bot-token-here",
    "prefix": "/"
}
```

## File Structure

```
jmusic-bot/
├── bot.py              # Main bot code
├── config.json         # Bot configuration
├── requirements.txt    # Python dependencies
├── playlists.json      # Playlist storage
├── ffmpeg.exe         # FFmpeg binary (Windows)
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

## Dependencies

- `discord.py>=2.3.0` - Discord API wrapper
- `yt-dlp>=2024.1.1` - YouTube/audio extraction
- `PyNaCl>=1.5.0` - Voice encryption
- `gTTS>=2.5.0` - Text-to-speech

## Hosting

For 24/7 hosting, consider:
- **VPS** (DigitalOcean, Linode, AWS)
- **PaaS** (Heroku, Railway, PythonAnywhere)
- **Docker** container deployment

## Security Notes

1. **Never commit `config.json` with real tokens**
2. Use environment variables in production
3. Keep `ffmpeg.exe` updated for security
4. Regularly update dependencies

## License

This project is for personal use. Ensure you comply with YouTube's Terms of Service and Discord's Developer Terms.

## Support

For issues and feature requests, please open an issue on GitHub.
## FFmpeg Setup

### For Local Development (Windows)
1. Download `ffmpeg.exe` from https://ffmpeg.org/download.html
2. Place it in the bot directory
3. The bot will automatically use it

### For Hosting (Linux/Mac)
Most hosting platforms already have FFmpeg installed system-wide. If not:

**Option 1: System installation**
```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y ffmpeg

# CentOS/RHEL
sudo yum install -y ffmpeg ffmpeg-devel
```

**Option 2: Use package manager**
Add to your deployment script:
```bash
# Check if ffmpeg exists
if ! command -v ffmpeg &> /dev/null; then
    echo "Installing FFmpeg..."
    # Add installation commands for your OS
fi
```

**Option 3: Python package**
The bot can also use `ffmpeg-python` package (added to requirements.txt).
## Troubleshooting

### "davey library needed in order to use voice" Error

This error occurs when PyNaCl (voice encryption library) is not properly installed.

**Solution:**

1. **Install system dependencies (Linux):**
   ```bash
   sudo apt-get update
   sudo apt-get install -y libffi-dev libssl-dev libsodium-dev python3-dev build-essential
   ```

2. **Reinstall PyNaCl:**
   ```bash
   pip uninstall PyNaCl -y
   pip install PyNaCl --no-cache-dir
   ```

3. **Alternative: Use discord.py[voice] package:**
   ```bash
   pip install discord.py[voice]
   ```

4. **For Docker/Railway/Heroku:** Add buildpacks or system packages for libsodium.