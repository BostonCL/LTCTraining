# Basketball Avatar Videos - Vercel Deployment Fix

## Problem
Your basketball avatar animation videos (`.mov` files) are stored in Git LFS and not being downloaded during Vercel deployment, causing them to be missing from the deployed site.

## Solution Applied

### 1. Updated Build Process
- Modified `package.json` to run LFS pull before building
- Added proper video file handling in `vercel.json`

### 2. Required Setup Steps

#### Step 1: Configure GitHub Token in Vercel
1. Go to your Vercel project dashboard
2. Navigate to **Settings → Environment Variables**
3. Add a new environment variable:
   - **Name**: `GITHUB_TOKEN`
   - **Value**: Your GitHub Personal Access Token (with `repo` scope)
   - **Environments**: Select all (Production, Preview, Development)
4. Click "Save"

#### Step 2: Create GitHub Personal Access Token (if you don't have one)
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name like "Vercel LFS Access"
4. Set expiration (recommend: No expiration or 1 year)
5. Select scopes:
   - ✅ `repo` (Full control of private repositories)
6. Click "Generate token"
7. **Copy the token immediately** (you won't be able to see it again!)

#### Step 3: Redeploy
After adding the environment variable:
1. Go to **Deployments** tab in Vercel
2. Click the three dots (⋮) on the latest deployment
3. Click "Redeploy"
4. Or simply push a new commit to trigger automatic deployment

## How It Works Now

The build process will:
1. **Download LFS files**: Run `scripts/pull-lfs.sh` to fetch all video files
2. **Authenticate with GitHub**: Use your `GITHUB_TOKEN` for private repository access
3. **Build the project**: Continue with normal SvelteKit build process
4. **Serve videos**: Videos will be available at `/static/images/*.mov`

## Expected Build Time
- **Before**: ~2-3 minutes
- **After**: ~5-10 minutes (due to downloading 4.6 GB of video files)

## Video File Locations
Your basketball avatar videos are located at:
- `static/images/ballSackIntroS1.mov`
- `static/images/ballSackIntroS12.mov`
- `static/images/ballSackm2Intro.mov`
- `static/images/ballSackm2s1.mov`
- `static/images/ballsackm2s2.mov`
- `static/images/ballsackm2s3.mov`
- `static/images/ballSackm2s4.mov`

## Troubleshooting

### Build Fails with "batch request: missing protocol"
- ✅ Make sure `GITHUB_TOKEN` is set in Vercel environment variables
- ✅ Verify the token has `repo` scope
- ✅ Check that the token hasn't expired

### Build Times Out
- The LFS files are large (4.6 GB total)
- Vercel has a 15-minute build timeout limit
- If it times out, consider optimizing video files or using a CDN

### Videos Still Don't Load
- Check browser console for 404 errors
- Verify video files exist in `static/images/` after build
- Check that video paths in your code match actual file locations
- Ensure videos are properly referenced in your Svelte components

### Alternative Solutions (if LFS continues to be problematic)

#### Option 1: Use a CDN
Upload videos to a CDN service like:
- Cloudflare R2
- AWS S3
- Google Cloud Storage
- Vercel Blob Storage

#### Option 2: Optimize Videos
- Convert `.mov` to `.webm` with alpha transparency
- Use video compression tools
- Consider using Lottie animations instead

#### Option 3: Use Git LFS with Different Hosting
- Consider using Netlify (has better LFS support)
- Or use a different deployment strategy

## Verification Steps

After deployment, check:
1. **Browser Console**: No 404 errors for video files
2. **Network Tab**: Videos load successfully
3. **Avatar Animations**: Basketball avatar animations play correctly
4. **File Sizes**: Videos are the expected size (not placeholder files)

## Support

If you continue to have issues:
1. Check Vercel build logs for LFS-related errors
2. Verify your GitHub token permissions
3. Consider the alternative solutions above
4. Contact Vercel support for LFS-specific issues
