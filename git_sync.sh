#!/bin/bash
cd /opt/sdmproxy || exit

echo "🔍 Checking for changes..."
git status

read -p "➡️  Continue with add + commit + push? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
  echo "❌ Cancelled."
  exit 0
fi

git add .
read -p "💬 Commit message: " MSG
git commit -m "$MSG"

echo "🔄 Pulling remote changes..."
git pull --rebase

echo "🚀 Pushing to GitHub..."
git push

echo "✅ Sync complete!"
