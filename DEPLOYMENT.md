# Deployment Guide

This guide explains how to deploy the JMusic bot to various hosting platforms.

## Prerequisites

1. **GitHub Repository**: Your bot code should be in a GitHub repository
2. **Discord Bot Token**: From Discord Developer Portal
3. **Hosting Account**: Choose one of the options below

## Hosting Options

### Option 1: VPS (Virtual Private Server)

**Recommended for: Full control, 24/7 uptime**

1. **Get a VPS** (DigitalOcean, Linode, AWS EC2, etc.)
2. **Connect via SSH**
3. **Install dependencies:**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and Git
   sudo apt install python3 python3-pip git ffmpeg -y
   
   # Clone your repository
   git clone https://github.com/username/jmusic-bot.git
   cd jmusic-bot
   
   # Install Python dependencies
   pip3 install -r requirements.txt
   ```

4. **Configure the bot:**
   ```bash
   cp config.example.json config.json
   nano config.json  # Add your Discord token
   ```

5. **Run with process manager (PM2 for Node.js style):**
   ```bash
   # Install PM2
   sudo npm install -g pm2
   
   # Start bot with PM2
   pm2 start "python3 bot.py" --name "jmusic-bot"
   
   # Save PM2 configuration
   pm2 save
   pm2 startup
   ```

### Option 2: Railway.app

**Recommended for: Easy deployment, free tier available**

1. **Create Railway account** at https://railway.app
2. **Create new project** → Deploy from GitHub repo
3. **Add environment variables:**
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```
4. **Configure Railway:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
5. **Deploy**

### Option 3: Heroku

**Recommended for: Free tier (with limitations)**

1. **Create Heroku account** at https://heroku.com
2. **Install Heroku CLI**
3. **Create `Procfile`:**
   ```
   worker: python bot.py
   ```
4. **Deploy:**
   ```bash
   heroku create jmusic-bot
   git push heroku main
   heroku config:set DISCORD_TOKEN=your_bot_token_here
   heroku ps:scale worker=1
   ```

### Option 4: PythonAnywhere

**Recommended for: Python-focused hosting**

1. **Create PythonAnywhere account** at https://pythonanywhere.com
2. **Upload files** via web interface or Git
3. **Install dependencies** in Bash console:
   ```bash
   pip install -r requirements.txt
   ```
4. **Create scheduled task** to run bot continuously

### Option 5: Replit

**Recommended for: Development and testing**

1. **Create Replit account** at https://replit.com
2. **Import from GitHub**
3. **Add Secrets:**
   - `DISCORD_TOKEN` = your bot token
4. **Configure .replit:**
   ```toml
   run = "python bot.py"
   ```
5. **Enable Always-On** (requires paid plan for 24/7)

## Environment Variables (Recommended)

For production, use environment variables instead of `config.json`:

1. **Modify `bot.py`** to check for environment variable:
   ```python
   import os
   
   # Try environment variable first, then config file
   token = os.environ.get('DISCORD_TOKEN')
   if not token:
       with open(CONFIG_PATH, 'r') as f:
           config = json.load(f)
       token = config['api_key']
   ```

2. **Update `config.json` reading** to handle both methods.

## Security Best Practices

1. **Never commit tokens** to GitHub
2. **Use environment variables** in production
3. **Regularly update dependencies:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```
4. **Monitor logs** for issues
5. **Set up backups** for playlist data

## Monitoring

1. **Uptime monitoring**: UptimeRobot, StatusCake
2. **Logs**: View application logs on your hosting platform
3. **Restart on failure**: Use PM2, systemd, or hosting platform features

## Troubleshooting

### Bot doesn't start
- Check Discord token is correct
- Verify all dependencies are installed
- Check Python version (3.8+ required)

### No audio in voice channels
- Ensure FFmpeg is installed
- Check bot has proper permissions
- Verify voice channel connectivity

### Commands not appearing
- Re-invite bot with `applications.commands` scope
- Wait for global command sync (can take up to 1 hour)
- Use guild-specific commands during development

## Maintenance

1. **Weekly**: Check dependency updates
2. **Monthly**: Review logs and performance
3. **As needed**: Update FFmpeg binary

## Support

For deployment issues:
1. Check hosting platform documentation
2. Review Discord.py documentation
3. Open GitHub issue with error details