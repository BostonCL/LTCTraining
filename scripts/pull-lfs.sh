#!/bin/bash
set -e

echo "Setting up Git LFS..."

# Ensure git lfs is installed
git lfs install

# Check if we're in Vercel build environment
if [ -n "$VERCEL" ]; then
  echo "Running in Vercel environment"
  
  # Get the current git remote URL
  REMOTE_URL=$(git config --get remote.origin.url || echo "")
  echo "Remote URL: $REMOTE_URL"
  
  # Configure Git LFS endpoint explicitly
  if [ -n "$REMOTE_URL" ]; then
    # Extract the repo path from the URL
    if [[ "$REMOTE_URL" =~ github\.com[:/](.+)\.git ]]; then
      REPO_PATH="${BASH_REMATCH[1]}"
      echo "Configuring LFS endpoint for repo: $REPO_PATH"
      
      # Set LFS endpoint using the same auth as git clone
      git config lfs.url "https://github.com/${REPO_PATH}.git/info/lfs"
    fi
  fi
  
  # If GITHUB_TOKEN is provided, use it for authentication
  if [ -n "$GITHUB_TOKEN" ]; then
    echo "Using GITHUB_TOKEN for authentication"
    git config lfs.url "https://${GITHUB_TOKEN}@github.com/BostonCL/LTCTraining.git/info/lfs"
  fi
fi

# Fetch LFS files
echo "Fetching Git LFS files..."
git lfs fetch --all

# Checkout LFS files
echo "Checking out Git LFS files..."
git lfs checkout

echo "Git LFS setup completed successfully!"

