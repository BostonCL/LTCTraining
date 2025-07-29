#!/bin/bash
set -e

# Install Git LFS
git lfs install

# Pull LFS files
git lfs pull

# Install dependencies
npm install

# Build the project
npm run build 