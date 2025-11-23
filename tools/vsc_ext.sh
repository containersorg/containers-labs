#!/usr/bin/env bash
# Author: Juan Medina
# Email: jumedina@redhat.com
# Date: Nov 2025

EXT_FILE="extensions.txt"

# Cause pipelines to return the exit status of the last command that failed (if any).
set -o pipefail

echo "Installing VS Code Extensions..."

if ! command -v code &> /dev/null; then
    echo "ERROR: 'code' command not found. Please ensure VS Code is installed and in your PATH."
    exit 1
fi

while IFS= read -r EXTENSION_ID; do
    if [[ -n "$EXTENSION_ID" && "${EXTENSION_ID:0:1}" != "#" ]]; then
        echo "Installing: ${EXTENSION_ID}..."
        code --install-extension "$EXTENSION_ID" --force
    fi
done < "$EXT_FILE"

echo "Extension installation process complete."
