#!/bin/bash
# .github/scripts/run-headless.sh
set -e

echo "🖥️ Starting Xvfb virtual display context for Pygame..."

# xvfb-run simulates an active screen layer (1280x1024, 24-bit color)
# -q hides the chatty pytest setup output but shows failures
xvfb-run --server-args="-screen 0 1280x1024x24" python -m pytest -q "$@"
