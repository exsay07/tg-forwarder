# Telegram Group Forwarder

Automatically forwards new messages from one Telegram group or channel to another using your own account. No bots required.

## Features

- Forwards text messages, photos, videos, files, voice messages
- Saves settings — no need to reconfigure on every launch
- Supports Two-Step Verification (2FA)
- Works on Windows and macOS

## Quick Start

### Windows
1. Double-click `start_windows.bat`

### macOS
```bash
chmod +x start_mac.sh
./start_mac.sh
```

## Setup Guides

- **Windows** → see `SETUP_WINDOWS.txt`
- **macOS** → see `SETUP_MAC.txt`

## Files

| File | Description |
|------|-------------|
| `forwarder.py` | Main script |
| `start_windows.bat` | Launcher for Windows |
| `start_mac.sh` | Launcher for macOS |
| `SETUP_WINDOWS.txt` | Step-by-step guide for Windows |
| `SETUP_MAC.txt` | Step-by-step guide for macOS |

## Requirements

- Python 3.8+
- [Telethon](https://github.com/LonamiWebs/Telethon) (`pip install telethon`)
- Telegram API credentials from [my.telegram.org/apps](https://my.telegram.org/apps)

## Change Groups

To select different source/target groups:

```bash
python forwarder.py --reset       # Windows
python3 forwarder.py --reset      # macOS
```

## Notes

- A session file `forwarder_session.session` is created after first login — do not delete it
- Settings are stored in `config.json`
- Add both files to `.gitignore` if you fork this repo
