#!/bin/bash

# Script to create .env files from .env.sample files
# Usage: ./scripts/create-env-files.sh

echo "Creating .env files from .env.sample files..."

# Root .env file
if [ -f ".env.sample" ] && [ ! -f ".env" ]; then
    cp .env.sample .env
    echo "✅ Created .env in project root"
else
    echo "⚠️  .env already exists in project root or .env.sample not found"
fi

# Account service .env
if [ -f "backend/services/account/.env.sample" ] && [ ! -f "backend/services/account/.env" ]; then
    cp backend/services/account/.env.sample backend/services/account/.env
    echo "✅ Created backend/services/account/.env"
else
    echo "⚠️  Account service .env already exists or .env.sample not found"
fi

# Notification service .env
if [ -f "backend/services/notification/.env.sample" ] && [ ! -f "backend/services/notification/.env" ]; then
    cp backend/services/notification/.env.sample backend/services/notification/.env
    echo "✅ Created backend/services/notification/.env"
else
    echo "⚠️  Notification service .env already exists or .env.sample not found"
fi

# Frontend .env
if [ -f "frontend/.env.sample" ] && [ ! -f "frontend/.env" ]; then
    cp frontend/.env.sample frontend/.env
    echo "✅ Created frontend/.env"
else
    echo "⚠️  Frontend .env already exists or .env.sample not found"
fi

echo ""
echo "📝 Please edit the .env files and update with your actual values!"
echo "   - Root .env: Contains all service configurations"
echo "   - Service-specific .env: Override specific service settings"

