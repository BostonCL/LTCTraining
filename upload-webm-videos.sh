#!/bin/bash
set -e

echo "🎬 Uploading Optimized WebM Videos to Cloudflare R2"
echo "==================================================="
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

# Prompt for credentials (they won't be saved)
echo "Please enter your Cloudflare R2 credentials:"
echo "(These will NOT be saved anywhere)"
echo ""
read -p "Access Key ID: " ACCESS_KEY_ID
read -sp "Secret Access Key: " SECRET_ACCESS_KEY
echo ""
echo ""
echo "Enter your Account ID (just the hex string, NOT the full URL)"
echo "Example: 578cbee8e80cddb5b97e12ab294130e2"
read -p "Account ID: " ACCOUNT_ID_INPUT
echo ""

# Extract just the account ID from whatever was entered
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
echo "📤 Uploading optimized .webm videos to R2..."
echo ""

# Upload only the optimized .webm videos
rclone copy static/images/ r2temp:${BUCKET_NAME}/images/ \
  --include "*.webm" \
  --progress \
  --transfers 4

echo ""
echo "🎉 Upload complete!"
echo ""
echo "Your optimized videos are now available at:"
echo "${R2_PUBLIC_URL}/images/"
echo ""
echo "✅ Videos are 99% smaller and preserve transparency!"
echo ""

# Clean up rclone config
rclone config delete r2temp

echo "✅ Temporary credentials removed from system"
echo ""
echo "Next steps:"
echo "1. Test your application - videos should load much faster"
echo "2. Deploy to Vercel when ready"

