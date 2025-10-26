#!/bin/bash

# Simple start script for CRM
# سكريبت بسيط لتشغيل نظام CRM

echo "🚀 Starting CRM System..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Start Django server in background
echo "📦 Starting Django server on port 8000..."
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Wait for server to start
sleep 3

# Start Cloudflare tunnel
echo "🌐 Starting Cloudflare Tunnel..."
echo ""
echo "⏳ Please wait for the public URL..."
echo ""

cloudflared tunnel --url http://localhost:8000

# Cleanup on exit
kill $DJANGO_PID 2>/dev/null

