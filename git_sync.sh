k#!/bin/bash
# Git sync script using SSH authentication

cd /opt/sdmproxy || exit

echo "📦 Adding changes..."
git add .

read -p "💬 Commit message: " MSG
git commit -m "$MSG"

echo "🔄 Pulling remote changes..."
git pull --rebase origin main

echo "🚀 Pushing to GitHub via SSH..."
git push origin main

echo "✅ Sync complete!"
