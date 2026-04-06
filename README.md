# tg-forwarder

Automatically forwards messages from one Telegram group/channel to another using your account. No bots needed.

## Requirements
- Python 3.8+
- Telegram API keys from [my.telegram.org/apps](https://my.telegram.org/apps)

## Run

**Windows** — double-click `start_windows.bat`

**macOS:**
```bash
chmod +x start_mac.sh
./start_mac.sh
```

## First Launch
The script will ask for your API ID, API Hash, phone number and a confirmation code from Telegram. After that — pick source and target groups from the list. Done.

## Reset groups
```bash
python forwarder.py --reset       # Windows
python3 forwarder.py --reset      # macOS
```

> ⚠️ Don't upload `config.json` and `*.session` to public repos — they contain your credentials.
