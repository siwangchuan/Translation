# AI Translation Assistant - Start Script for Windows PowerShell
# This script starts the backend server

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  AI Translation Assistant - Backend" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python is not installed. Please install Python 3.10 or higher." -ForegroundColor Red
    exit 1
}

# Check Python version
$pythonVersion = (python --version 2>&1).ToString()
Write-Host "Python version: $pythonVersion"

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\Activate.ps1") {
    & ".\venv\Scripts\Activate.ps1"
} else {
    Write-Host "Error: Could not find activation script." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt

# Check for environment variables
if (-not $env:ALIYUN_API_KEY) {
    Write-Host ""
    Write-Host "Warning: ALIYUN_API_KEY environment variable is not set." -ForegroundColor Yellow
    Write-Host "The translation service may not work properly."
    Write-Host "Please set it with: `$env:ALIYUN_API_KEY='your-api-key'"
    Write-Host ""
}

# Start the server
Write-Host ""
Write-Host "Starting backend server on http://localhost:8000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Green
Write-Host ""

Set-Location backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
