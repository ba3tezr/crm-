#!/bin/bash

# ========================================
# CRM System - Quick Start Script
# نظام CRM - سكريبت التشغيل السريع
# ========================================

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   CRM System - نظام إدارة العقارات${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}🔄 Activating virtual environment...${NC}"
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/.requirements_installed" ]; then
    echo -e "${YELLOW}📦 Installing requirements...${NC}"
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    touch venv/.requirements_installed
    echo -e "${GREEN}✅ Requirements installed${NC}"
fi

# Run migrations if needed
echo -e "${BLUE}🔄 Checking database migrations...${NC}"
python manage.py migrate --noinput 2>&1 | grep -q "No migrations to apply" && echo -e "${GREEN}✅ Database is up to date${NC}" || echo -e "${YELLOW}⚠️  Migrations applied${NC}"

# Collect static files
echo -e "${BLUE}🔄 Collecting static files...${NC}"
python manage.py collectstatic --noinput > /dev/null 2>&1
echo -e "${GREEN}✅ Static files collected${NC}"

# Compile messages
echo -e "${BLUE}🔄 Compiling translations...${NC}"
python manage.py compilemessages > /dev/null 2>&1
echo -e "${GREEN}✅ Translations compiled${NC}"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}🚀 Starting Django Server...${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Kill any existing Django processes on port 8000
lsof -ti:8000 | xargs kill -9 2>/dev/null

# Start Django server in background
python manage.py runserver 0.0.0.0:8000 > /dev/null 2>&1 &
DJANGO_PID=$!

# Wait for Django to start
echo -e "${YELLOW}⏳ Waiting for Django server to start...${NC}"
sleep 3

# Check if Django is running
if ! curl -s http://localhost:8000 > /dev/null; then
    echo -e "${RED}❌ Failed to start Django server${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Django server started on http://localhost:8000${NC}"
echo ""

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo -e "${RED}❌ cloudflared is not installed${NC}"
    echo -e "${YELLOW}Installing cloudflared...${NC}"
    
    # Detect OS and install cloudflared
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
        sudo dpkg -i cloudflared-linux-amd64.deb
        rm cloudflared-linux-amd64.deb
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install cloudflared
    else
        echo -e "${RED}❌ Unsupported OS. Please install cloudflared manually${NC}"
        echo "Visit: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/"
        exit 1
    fi
    
    echo -e "${GREEN}✅ cloudflared installed${NC}"
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}🌐 Starting Cloudflare Tunnel...${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Kill any existing cloudflared processes
pkill -f cloudflared 2>/dev/null

# Start cloudflared tunnel
echo -e "${YELLOW}⏳ Creating temporary public URL...${NC}"
echo ""

# Run cloudflared and capture output
cloudflared tunnel --url http://localhost:8000 2>&1 | while IFS= read -r line; do
    echo "$line"
    
    # Extract and highlight the public URL
    if echo "$line" | grep -q "https://.*\.trycloudflare.com"; then
        URL=$(echo "$line" | grep -oP 'https://[^\s]+\.trycloudflare.com')
        echo ""
        echo -e "${BLUE}========================================${NC}"
        echo -e "${GREEN}✅ Application is now live!${NC}"
        echo -e "${BLUE}========================================${NC}"
        echo ""
        echo -e "${GREEN}🌐 Public URL: ${YELLOW}$URL${NC}"
        echo ""
        echo -e "${BLUE}📋 Default Credentials:${NC}"
        echo -e "   Username: ${YELLOW}admin${NC}"
        echo -e "   Password: ${YELLOW}admin123${NC}"
        echo ""
        echo -e "${BLUE}📋 Test Tenant:${NC}"
        echo -e "   Username: ${YELLOW}majed${NC}"
        echo -e "   Password: ${YELLOW}majed123${NC}"
        echo ""
        echo -e "${YELLOW}⚠️  This is a temporary URL and will expire when you stop the script${NC}"
        echo -e "${RED}⚠️  Press Ctrl+C to stop the server${NC}"
        echo ""
        echo -e "${BLUE}========================================${NC}"
    fi
done

# Cleanup on exit
trap cleanup EXIT

cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Stopping servers...${NC}"
    kill $DJANGO_PID 2>/dev/null
    pkill -f cloudflared 2>/dev/null
    echo -e "${GREEN}✅ Servers stopped${NC}"
}

