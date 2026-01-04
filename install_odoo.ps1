param(
    [string]$OdooVersion = "16.0",
    [string]$TargetDirectory = "odoo_installation",
    [string]$GeminiApiKey = ""
)

$ErrorActionPreference = "Stop"

Write-Host "=== Odoo Windows Installer ===" -ForegroundColor Cyan
Write-Host "This script will download Odoo, install Python dependencies, and" -ForegroundColor Cyan
Write-Host "start the Odoo server on http://localhost:8069 (if successful)." -ForegroundColor Cyan

# Move to the directory where this script lives so relative paths work.
Set-Location -Path $PSScriptRoot

# 1. Ensure Python is available
Write-Host "Checking for Python..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Error: Python is not installed or not on PATH." -ForegroundColor Red
    Write-Host "Please install Python 3, then run this script again." -ForegroundColor Red
    exit 1
}
Write-Host "Python found at $($python.Source)" -ForegroundColor Green

# 2. Install Python dependencies for the agent itself
Write-Host "Installing Python dependencies for the installer agent..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 3. Export optional Gemini API key for the agent
if ($GeminiApiKey -ne "") {
    Write-Host "Configuring GEMINI_API_KEY for Google Gemini integration..." -ForegroundColor Yellow
    $env:GEMINI_API_KEY = $GeminiApiKey
}

# 4. Run the Python agent to perform the real Odoo installation
Write-Host "Running Odoo installer agent..." -ForegroundColor Yellow
# main.py internally sets real_install=True
python main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "=== Odoo installer finished. ===" -ForegroundColor Green
    Write-Host "If everything succeeded, open http://localhost:8069 in your browser." -ForegroundColor Green
} else {
    Write-Host "Installer script completed, but the agent reported errors." -ForegroundColor Red
    Write-Host "Check the output above for details." -ForegroundColor Red
}
