# Avacta News Alert

Monitors the Avacta (AVCT) RSS feed and sends Telegram notifications when new articles are published.

## How It Works

1. A GitHub Actions cron job runs every 5 minutes
2. The script fetches the Avacta RSS feed at `https://avacta.com/feed/`
3. If there's a new article (different from what's saved in `last_seen.txt`), it sends a Telegram notification
4. The `last_seen.txt` file is automatically committed back to the repo

## Setup

### 1. Create a Telegram Bot

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the prompts
3. Save the bot token (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Get Your Chat ID

1. Message your new bot (send `/start` or any message)
2. Visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Find your chat ID in the response under `"chat":{"id":...}`

### 3. Configure GitHub Secrets

Go to your repo → Settings → Secrets and variables → Actions, then add:

- `TELEGRAM_BOT_TOKEN` - Your bot token from BotFather
- `TELEGRAM_CHAT_ID` - Your chat ID

### 4. Enable GitHub Actions

The workflow will start automatically. Check the Actions tab to verify it's running.

## Testing

To verify your Telegram configuration:

1. Go to Actions → "Check Avacta News" → "Run workflow"
2. Check "Send test message to verify Telegram"
3. Click "Run workflow"
4. You should receive a test message on Telegram

## Files

- `checker.py` - Main script that checks the RSS feed and sends notifications
- `last_seen.txt` - Stores the URL of the last seen article (auto-updated)
- `.github/workflows/check-news.yml` - GitHub Actions workflow configuration
- `requirements.txt` - Python dependencies

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"

# Run the checker
python checker.py

# Run in test mode
python checker.py --test
```

## License

MIT
