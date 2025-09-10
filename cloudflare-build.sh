#!/bin/bash

# Cloudflare Pages build script for Digital Garden
# This script handles the custom plugins that won't work on GitHub Pages

echo "🚀 Starting Cloudflare Pages build for Digital Garden..."

# Install Ruby gems
echo "📦 Installing dependencies..."
bundle install

# Build the Jekyll site
echo "🏗️  Building Jekyll site..."
JEKYLL_ENV=production bundle exec jekyll build --verbose

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build completed successfully!"
    echo "📁 Site built in _site/ directory"
    ls -la _site/
else
    echo "❌ Build failed!"
    exit 1
fi