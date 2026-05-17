#!/bin/bash
# 研墨 (YanMo) — one-line install script
# curl -fsSL https://raw.githubusercontent.com/sixtdreanight/Yanmo/master/scripts/install.sh | bash

set -e

echo "=== 研墨 YanMo Installer ==="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Python 3.11+ required. Install it first: https://python.org"
    exit 1
fi

# Check Node
if ! command -v node &> /dev/null; then
    echo "Node.js 18+ required. Install it first: https://nodejs.org"
    exit 1
fi

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found. Install it: curl -fsSL https://ollama.com/install.sh | sh"
    exit 1
fi

INSTALL_DIR="${YANMO_HOME:-$HOME/.yanmo}"

echo "Installing to $INSTALL_DIR..."

# Clone or pull
if [ -d "$INSTALL_DIR/repo" ]; then
    cd "$INSTALL_DIR/repo"
    git pull --ff-only origin master
else
    mkdir -p "$INSTALL_DIR"
    git clone https://github.com/sixtdreanight/Yanmo.git "$INSTALL_DIR/repo"
    cd "$INSTALL_DIR/repo"
fi

pip install -e ".[dev]" --quiet
cd frontend && npm install --silent

echo ""
echo "Installed. Start with:"
echo "  python -m backend.main"
echo "  cd $INSTALL_DIR/repo/frontend && npm run dev"
echo ""
echo "Or build the desktop app:"
echo "  cd $INSTALL_DIR/repo/frontend && cargo tauri build"
