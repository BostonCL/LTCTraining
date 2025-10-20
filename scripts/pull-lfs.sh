#!/bin/bash
set -e

echo "Setting up Git LFS..."

# Ensure git lfs is installed
git lfs install

# Check if we're in Vercel build environment
if [ -n "$VERCEL" ]; then
  echo "Running in Vercel environment"
  
  # Get the current git remote URL
  REMOTE_URL=$(git config --get remote.origin.url 2>/dev/null || echo "")
  echo "Remote URL: $REMOTE_URL"
  
  # If remote URL is empty or missing, set it explicitly
  if [ -z "$REMOTE_URL" ]; then
    echo "Remote URL not found, setting it explicitly..."
    git remote add origin https://github.com/BostonCL/LTCTraining.git 2>/dev/null || true
    git remote set-url origin https://github.com/BostonCL/LTCTraining.git
    REMOTE_URL="https://github.com/BostonCL/LTCTraining.git"
    echo "Set remote URL to: $REMOTE_URL"
  fi
  
  # Configure Git LFS endpoint
  if [ -n "$GITHUB_TOKEN" ]; then
    echo "Using GITHUB_TOKEN for authentication"
    git config lfs.url "https://${GITHUB_TOKEN}@github.com/BostonCL/LTCTraining.git/info/lfs"
    echo "LFS URL configured with authentication (token hidden for security)"
  else
    echo "No GITHUB_TOKEN found, using public access"
    git config lfs.url "https://github.com/BostonCL/LTCTraining.git/info/lfs"
    echo "LFS URL configured: $(git config lfs.url)"
  fi
fi

# Fetch LFS files
echo "Fetching Git LFS files..."
git lfs fetch --all

# Checkout LFS files
echo "Checking out Git LFS files..."
git lfs checkout

echo "Git LFS setup completed successfully!"

