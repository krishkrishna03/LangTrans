#!/bin/bash

# LangTrans Quick Start Setup Script
# This script sets up the entire LangTrans application

set -e

echo "🌐 LangTrans - Universal Language Translator"
echo "=============================================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "⚠️  Docker Compose is not installed. Installing via Docker plugin..."
fi

echo "✅ Docker is installed"
echo ""

# Clone/Setup
echo "📁 Setting up project directories..."
mkdir -p backend frontend

# Backend setup
echo "🔧 Setting up backend..."
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "✅ Backend .env created"
fi

# Frontend setup
echo "🎨 Setting up frontend..."
if [ ! -f frontend/.env ]; then
    cp frontend/.env.example frontend/.env
    echo "✅ Frontend .env created"
fi

echo ""
echo "🚀 Starting services with Docker Compose..."
echo "This may take a few minutes on first run (downloading models)..."
echo ""

docker-compose up --build

echo ""
echo "✅ Setup complete!"
echo ""
echo "📍 Access the application:"
echo "   Frontend:  http://localhost:3000"
echo "   API:       http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "💡 Tip: Press Ctrl+C to stop the services"
