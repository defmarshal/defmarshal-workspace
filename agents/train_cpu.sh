#!/bin/bash
# Activate venv and run training with simple PEFT script
set -e

VENV="/home/ubuntu/.openclaw/workspace/.venv"
SCRIPT="/home/ubuntu/.openclaw/workspace/agents/train_lora_simple.py"

if [ ! -d "$VENV" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV"
fi

source "$VENV/bin/activate"

# Install dependencies if not present
pip install -q transformers peft bitsandbytes datasets torch 2>/dev/null || {
    echo "Installing dependencies..."
    pip install transformers peft bitsandbytes datasets torch
}

echo "Starting training..."
python3 "$SCRIPT" "$@"
