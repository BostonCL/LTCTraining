# CDN Migration Plan for Basketball Avatar Videos

## Current Problem
- GitHub LFS budget exceeded (4.6 GB of videos)
- LFS costs $50/month for 10 GB
- Videos are blocking deployment

## Recommended Solution: Move to Cloudflare R2

### Why Cloudflare R2?
- ✅ **Much cheaper**: ~$0.015/GB/month vs $5/GB/month for GitHub LFS
- ✅ **Better performance**: Global CDN
- ✅ **No bandwidth charges**: Unlike AWS S3
- ✅ **Easy integration**: Works with Vercel

### Cost Comparison
- **GitHub LFS**: $50/month for 10 GB
- **Cloudflare R2**: ~$0.07/month for 4.6 GB (99.9% cheaper!)

## Migration Steps

### Step 1: Set Up Cloudflare R2
1. Create Cloudflare account (free)
2. Go to R2 Object Storage
3. Create a new bucket: `ltctraining-videos`
4. Get API credentials

### Step 2: Upload Videos to R2
```bash
# Install R2 CLI
npm install -g wrangler

# Upload videos
wrangler r2 object put ltctraining-videos/ballSackIntroS1.mov --file=static/images/ballSackIntroS1.mov
wrangler r2 object put ltctraining-videos/ballSackIntroS12.mov --file=static/images/ballSackIntroS12.mov
# ... repeat for all videos
```

### Step 3: Update Video URLs in Code
Replace local video paths with R2 URLs:
```javascript
// Before
const videoUrl = '/static/images/ballSackIntroS1.mov';

// After  
const videoUrl = 'https://your-bucket.your-account.r2.cloudflarestorage.com/ballSackIntroS1.mov';
```

### Step 4: Remove from Git LFS
```bash
# Remove videos from LFS tracking
git lfs untrack "static/images/*.mov"
git rm --cached "static/images/*.mov"
git add .gitattributes
git commit -m "Remove videos from LFS, now served from CDN"
```

## Alternative CDN Options

### Option A: Vercel Blob Storage
- **Cost**: $0.15/GB/month
- **Pros**: Native Vercel integration
- **Cons**: More expensive than R2

### Option B: AWS S3 + CloudFront
- **Cost**: ~$0.10/GB/month + bandwidth
- **Pros**: Very reliable
- **Cons**: More complex setup

### Option C: Google Cloud Storage
- **Cost**: ~$0.02/GB/month
- **Pros**: Good pricing
- **Cons**: More setup required

## Quick Fix (Temporary)
If you need videos working immediately:

1. **Compress videos** to reduce size:
   ```bash
   # Reduce quality to fit in free LFS (1 GB)
   ffmpeg -i input.mov -crf 28 -preset fast output.mov
   ```

2. **Use different format** (WebM with alpha):
   ```bash
   # Convert to WebM with alpha transparency
   ffmpeg -i input.mov -c:v libvpx-vp9 -pix_fmt yuva420p output.webm
   ```

## Recommended Action
**Move to Cloudflare R2** - it's the most cost-effective solution and will save you $600/year compared to GitHub LFS.
