#!/bin/bash
### Modified to deploy a specific HTML page from GitHub

Green="\033[32m"
Red="\033[31m"
Yellow="\033[33m"
Blue="\033[36m"
Font="\033[0m"
OK="${Green}[OK]${Font}"
ERROR="${Red}[ERROR]${Font}"

function msg_inf() {  echo -e "${Blue}$1${Font}"; }
function msg_ok() { echo -e "${OK} ${Blue}$1${Font}"; }
function msg_err() { echo -e "${ERROR} ${Yellow}$1${Font}"; }

# URL of the target HTML file
TARGET_URL="https://raw.githubusercontent.com/mynameisvyach/install/main/index.html"
DEST_DIR="/var/www/html"
DEST_FILE="$DEST_DIR/index.html"

msg_inf "Starting deployment of the new web page..."

# Check if destination directory exists, if not, create it
if [[ ! -d "$DEST_DIR" ]]; then
    msg_inf "Directory $DEST_DIR does not exist. Creating it..."
    mkdir -p "$DEST_DIR"
    if [[ $? -ne 0 ]]; then
        msg_err "Failed to create directory $DEST_DIR. Please check permissions."
        exit 1
    fi
fi

# Backup current index.html if it exists
if [[ -f "$DEST_FILE" ]]; then
    BACKUP_FILE="$DEST_FILE.backup.$(date +%Y%m%d%H%M%S)"
    msg_inf "Backing up current index.html to $BACKUP_FILE"
    cp "$DEST_FILE" "$BACKUP_FILE"
    if [[ $? -ne 0 ]]; then
        msg_err "Failed to create a backup. Please check write permissions."
        exit 1
    fi
fi

# Download the new index.html
msg_inf "Downloading new web page from $TARGET_URL"
wget -q -O "$DEST_FILE" "$TARGET_URL"

# Check if download was successful
if [[ $? -eq 0 && -f "$DEST_FILE" ]]; then
    msg_ok "Web page successfully downloaded and installed to $DEST_FILE"
else
    msg_err "Failed to download the web page. Please check your internet connection and the URL."
    # Attempt to restore backup if it exists
    if [[ -f "$BACKUP_FILE" ]]; then
        msg_inf "Restoring the previous version from backup..."
        mv "$BACKUP_FILE" "$DEST_FILE"
        msg_ok "Previous version restored."
    fi
    exit 1
fi

# Set appropriate permissions (optional, but a good practice)
chmod 644 "$DEST_FILE"
msg_ok "Permissions set to 644 for $DEST_FILE"

msg_ok "Deployment complete! Your web page is now live."
exit 0
