# Test quick shortcut creation script for quickly access links via launcher

```
#!/usr/bin/env bash

set -e

# Where shortcuts will be stored
SHORTCUT_DIR="$HOME/.local/share/drive-shortcuts"
DESKTOP_FILE_DIR="$HOME/.local/share/applications"

mkdir -p "$SHORTCUT_DIR"
mkdir -p "$DESKTOP_FILE_DIR"

echo "=== Create Linux Web Shortcut (.desktop) ==="

# Ask for inputs
read -rp "Name: " NAME
read -rp "Full URL: " URL
read -rp "Tags (space or comma separated): " TAGS

# Sanitize filename
SAFE_NAME=$(echo "$NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9_-]/-/g')

DESKTOP_FILE="$SHORTCUT_DIR/${SAFE_NAME}.desktop"

ICON="folder"

# Create .desktop file
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Type=Link
Name=$NAME
URL=$URL
Icon=$ICON
Comment=Tags: $TAGS
EOF

chmod +x "$DESKTOP_FILE"

# Optional: symlink into applications for launcher visibility
ln -sf "$DESKTOP_FILE" "$DESKTOP_FILE_DIR/${SAFE_NAME}.desktop"

# Create or append tag index for searching
TAG_INDEX="$SHORTCUT_DIR/.tags-index"

echo "$NAME | $URL | $TAGS" >> "$TAG_INDEX"

echo ""
echo "✅ Shortcut created!"
echo "📁 File: $DESKTOP_FILE"
echo "🚀 Available in app launcher (if supported)"
echo "🏷️ Tags indexed in: $TAG_INDEX"
```
