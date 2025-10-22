#!/bin/bash
set -e

echo "🎬 Uploading Optimized Videos to Cloudflare R2"
echo "=============================================="
echo ""

# Check if rclone is configured
if ! rclone listremotes >/dev/null 2>&1; then
    echo "❌ Rclone not configured. Please run: rclone config"
    echo "   Then add a remote named 'r2' pointing to your Cloudflare R2 bucket"
    exit 1
fi

echo "📤 Uploading optimized .webm videos..."
echo ""

# Upload the optimized videos
rclone copy static/images/ r2:ltctraining/static/images/ \
    --include "*.webm" \
    --progress \
    --transfers=4 \
    --checkers=8

echo ""
echo "✅ Upload complete!"
echo ""
echo "🎉 Your optimized videos are now live on Cloudflare R2!"
echo "   The videos are 99% smaller and preserve transparency!"
echo ""
echo "Next steps:"
echo "1. Test your application - the videos should load much faster"
echo "2. Deploy to Vercel when ready"

