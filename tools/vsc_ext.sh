#!/usr/bin/env bash
# Author: Juan Medina
# Email: jumedina@redhat.com
# Date: Nov 2025

# URL pointing to the extensions file on GitHub
EXT_URL="https://raw.githubusercontent.com/containersorg/containers-labs/refs/heads/main/tools/extensions.txt"

# Cause pipelines to return the exit status of the last command that failed (if any).
set -o pipefail

echo "Starting VS Code Extension Installation"

if ! command -v code &> /dev/null; then
    echo "ERROR: 'code' command not found. Please ensure VS Code is installed and in your PATH."
    exit 1
fi

curl -sL "$EXT_URL" | while IFS= read -r EXTENSION_ID
do
    EXTENSION_ID=$(echo "$EXTENSION_ID" | xargs)

    if [[ -n "$EXTENSION_ID" && "${EXTENSION_ID:0:1}" != "#" ]]
	 then
        echo "Installing: ${EXTENSION_ID}..."
        code --install-extension "$EXTENSION_ID" --force
    fi
done

echo "Extension installation process complete."
