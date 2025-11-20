#!/bin/bash
# Author: Juan Medina
# Date: Mar 2025
# Description: Setup Linux Class System

# Cause pipelines to return the exit status of the last command that failed.
set -o pipefail

# --- Configuration ---
PLAYBOOK_URL="https://raw.githubusercontent.com/containersorg/containers-labs/refs/heads/main/tools/class-setup.yml"
# Tags to run from the playbook
PLAYBOOK_TAGS="repos,container_packages,extra_packages,configurations,security,cockpit,looks,background,containers_looks,final"
# --- End Configuration ---

# === Pre-flight Checks ===

# 1. Check for root privileges
if [[ ${UID} -ne 0 ]]; then
    echo "Error: This script must be executed with sudo." >&2
    exit 1
fi

# 2. Check if running in a live environment
if id "liveuser" &>/dev/null || [[ -f /etc/live-release ]] || [[ "$(findmnt -n -o FSTYPE / || true )" =~ (squashfs|overlay) ]]; then
    echo "Error: This script should not be run as the 'liveuser' or from the live ISO environment." >&2
    echo "Please complete the Fedora installation and log in as a regular user before running this script." >&2
    exit 1
fi

# 3. Check if running on Fedora
if ! grep -q '^ID=fedora$' /etc/os-release || [[ ! -f /etc/fedora-release ]] || ! command -v dnf &>/dev/null; then
    echo "Error: This script is designed to run on Fedora Linux only." >&2
    echo "Please run this script on a Fedora Linux System." >&2
    exit 1
fi

# 4. Check for internet connectivity (using curl to check Google)
if [[ $(wget -q --spider http://google.com || true ; echo $?) -ne 0 ]]; then
    echo "Internet connection required"
    exit 2
fi

# === Setup ===

# 5. Install required packages
echo "Preflight configuration..."
dnf install -yq ansible git figlet lolcat curl

# 6. Prepare visuals
clear
echo "Starting Linux Setup process..."
sleep 5
figlet "Linux Setup" | lolcat

# 7. Download the playbook to a temporary file
# Create a secure temporary file
TEMP_PLAYBOOK=$(mktemp /tmp/class-setup.XXXXXX.yml)
# Ensure temp file is removed on script exit (normal, error, or interrupt)
# trap 'rm -f "$TEMP_PLAYBOOK"' EXIT
# Download using curl: -f fail on server errors, -L follow redirects, -o output to file
if ! curl -fL --connect-timeout 15 --max-time 60 -o "${TEMP_PLAYBOOK}" "${PLAYBOOK_URL}"; then
    echo "Error: Failed to download playbook from ${PLAYBOOK_URL}" >&2
    exit 3
fi

# === Execution ===

ansible-playbook "${TEMP_PLAYBOOK}" --tags "${PLAYBOOK_TAGS}"

# === Completion ===

figlet "Setup completed!" | lolcat
echo "The system will automatically reboot in 20 seconds..."
echo "      press Ctrl+c if you need to cancel the reboot process"
sleep 20
echo "Rebooting now!"
rm -rf /tmp/class-setup.yml
reboot
