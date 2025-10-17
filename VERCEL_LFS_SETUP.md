# Vercel Git LFS Setup Instructions

## Problem
Vercel doesn't automatically download Git LFS files during deployment, which causes basketball avatar videos to not load.

## Solution
Configure Vercel to authenticate with GitHub LFS using a GitHub Personal Access Token.

## Setup Steps

### 1. Create a GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name like "Vercel LFS Access"
4. Set expiration (recommend: No expiration or 1 year)
5. Select scopes:
   - ✅ `repo` (Full control of private repositories)
6. Click "Generate token"
7. **Copy the token immediately** (you won't be able to see it again!)

### 2. Add Token to Vercel

1. Go to your Vercel project dashboard
2. Navigate to: **Settings → Environment Variables**
3. Add a new environment variable:
   - **Name**: `GITHUB_TOKEN`
   - **Value**: Paste your GitHub Personal Access Token
   - **Environments**: Select all (Production, Preview, Development)
4. Click "Save"

### 3. Redeploy

After adding the environment variable:
1. Go to **Deployments** tab
2. Click the three dots (⋮) on the latest deployment
3. Click "Redeploy"
4. Or simply push a new commit to trigger automatic deployment

## How It Works

The build script (`scripts/pull-lfs.sh`) will:
1. Detect Vercel environment
2. Use the `GITHUB_TOKEN` to authenticate with GitHub LFS
3. Download all video files (4.6 GB) before building
4. Build process continues with all videos available

## Build Time
Expect the build to take 5-10 minutes longer due to downloading 4.6 GB of video files.

## Alternative: Public Repository
If your repository is public, you might not need the token. The script will attempt to access LFS without authentication first.

## Troubleshooting

**Build fails with "batch request: missing protocol"**
- Make sure `GITHUB_TOKEN` is set in Vercel environment variables
- Verify the token has `repo` scope
- Check that the token hasn't expired

**Build times out**
- LFS files might be too large
- Consider optimizing video files or using a CDN instead

**Videos still don't load**
- Check browser console for 404 errors
- Verify video files exist in `static/images/` after build
- Check that video paths in code match actual file locations

