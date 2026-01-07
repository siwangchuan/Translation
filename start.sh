#!/bin/bash

# AI Translation Assistant - Start Script for Linux/Mac
# This script starts the backend server

set -e

echo "=========================================="
echo "  AI Translation Assistant - Backend"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check for environment variables
if [ -z "$ALIYUN_API_KEY" ]; then
    echo ""
    echo "Warning: ALIYUN_API_KEY environment variable is not set."
    echo "The translation service may not work properly."
    echo "Please set it with: export ALIYUN_API_KEY='your-api-key'"
    echo ""
fi

# Start the server
echo ""
echo "Starting backend server on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""

cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
