#!/bin/bash

echo "========================================"
echo "   TELEGRAM GROUP FORWARDER"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed."
    echo "Install it via Homebrew: brew install python"
    echo "Or download from: https://www.python.org/downloads/"
    exit 1
fi

# Install telethon if not installed
echo "Checking dependencies..."
python3 -c "import telethon" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing telethon..."
    pip3 install telethon
fi

echo ""
echo "Starting forwarder..."
echo ""
python3 forwarder.py "$@"
