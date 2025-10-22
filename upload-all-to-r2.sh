#!/bin/bash
set -e

echo "🚀 Cloudflare R2 COMPLETE Upload Script"
echo "======================================"
echo ""
echo "This will upload ALL audio, video, and image files to R2"
echo ""

# Configuration
BUCKET_NAME="ltctraining-videos"
R2_PUBLIC_URL="https://pub-aca3ec806e844324a6218bb0d8bf7295.r2.dev"

# Check if rclone is installed
if ! command -v rclone &> /dev/null; then
    echo "❌ rclone is not installed."
    echo "Install it with: brew install rclone"
    exit 1
fi

# Prompt for credentials
echo "Please enter your Cloudflare R2 credentials:"
echo "(These will NOT be saved anywhere)"
echo ""
read -p "Access Key ID: " ACCESS_KEY_ID
read -sp "Secret Access Key: " SECRET_ACCESS_KEY
echo ""
echo ""
echo "Enter your Account ID (just the hex string)"
read -p "Account ID: " ACCOUNT_ID_INPUT
echo ""

# Extract account ID
ACCOUNT_ID=$(echo "$ACCOUNT_ID_INPUT" | sed -E 's|https?://||g' | sed 's|\.r2\.cloudflarestorage\.com.*||g' | sed 's|/.*||g')
echo "Using Account ID: $ACCOUNT_ID"
echo ""

# Configure rclone temporarily
echo "Configuring rclone..."
rclone config create r2temp s3 \
  provider Cloudflare \
  access_key_id "$ACCESS_KEY_ID" \
  secret_access_key "$SECRET_ACCESS_KEY" \
  endpoint "https://${ACCOUNT_ID}.r2.cloudflarestorage.com" \
  acl private

echo ""
echo "✅ Configuration complete!"
echo ""

# Upload ALL video files from static/images/
echo "📤 1/3: Uploading video files..."
rclone copy static/images/ r2temp:${BUCKET_NAME}/images/ \
  --include "*.mp4" \
  --include "*.mov" \
  --include "*.webm" \
  --progress \
  --transfers 4

echo ""
echo "📤 2/3: Uploading image files (jpg, png, webp)..."
rclone copy static/images/ r2temp:${BUCKET_NAME}/images/ \
  --include "*.jpg" \
  --include "*.png" \
  --include "*.webp" \
  --include "*.gif" \
  --progress \
  --transfers 8

echo ""
echo "📤 3/3: Uploading ALL audio files (mp3)..."
rclone copy static/audio/ r2temp:${BUCKET_NAME}/audio/ \
  --include "*.mp3" \
  --include "*.mp4" \
  --include "*.mov" \
  --progress \
  --transfers 8

echo ""
echo "🎉 Upload complete!"
echo ""
echo "Your assets are now available at:"
echo "${R2_PUBLIC_URL}/images/"
echo "${R2_PUBLIC_URL}/audio/"
echo ""

# Clean up
rclone config delete r2temp

echo "✅ Temporary credentials removed"
echo ""
echo "Files uploaded:"
echo "  - Videos: *.mp4, *.mov, *.webm"
echo "  - Images: *.jpg, *.png, *.webp, *.gif"
echo "  - Audio: *.mp3"


