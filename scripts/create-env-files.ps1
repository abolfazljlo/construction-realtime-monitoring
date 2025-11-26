# PowerShell script to create .env files from ENV_SAMPLE.txt files
# Usage: .\scripts\create-env-files.ps1

Write-Host "Creating .env files from ENV_SAMPLE.txt files..." -ForegroundColor Cyan

# Root .env file
if (Test-Path "ENV_SAMPLE.txt") {
    if (-not (Test-Path ".env")) {
        Copy-Item "ENV_SAMPLE.txt" ".env"
        Write-Host "✅ Created .env in project root" -ForegroundColor Green
    } else {
        Write-Host "⚠️  .env already exists in project root" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  ENV_SAMPLE.txt not found in project root" -ForegroundColor Yellow
}

# Account service .env
$accountEnvSample = "backend\services\account\ENV_SAMPLE.txt"
$accountEnv = "backend\services\account\.env"
if (Test-Path $accountEnvSample) {
    if (-not (Test-Path $accountEnv)) {
        Copy-Item $accountEnvSample $accountEnv
        Write-Host "✅ Created $accountEnv" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Account service .env already exists" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Account service ENV_SAMPLE.txt not found" -ForegroundColor Yellow
}

# Notification service .env
$notificationEnvSample = "backend\services\notification\ENV_SAMPLE.txt"
$notificationEnv = "backend\services\notification\.env"
if (Test-Path $notificationEnvSample) {
    if (-not (Test-Path $notificationEnv)) {
        Copy-Item $notificationEnvSample $notificationEnv
        Write-Host "✅ Created $notificationEnv" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Notification service .env already exists" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Notification service ENV_SAMPLE.txt not found" -ForegroundColor Yellow
}

# Frontend .env
$frontendEnvSample = "frontend\ENV_SAMPLE.txt"
$frontendEnv = "frontend\.env"
if (Test-Path $frontendEnvSample) {
    if (-not (Test-Path $frontendEnv)) {
        Copy-Item $frontendEnvSample $frontendEnv
        Write-Host "✅ Created $frontendEnv" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Frontend .env already exists" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Frontend ENV_SAMPLE.txt not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Please edit the .env files and update with your actual values!" -ForegroundColor Cyan
Write-Host "   - Root .env: Contains all service configurations" -ForegroundColor Gray
Write-Host "   - Service-specific .env: Override specific service settings" -ForegroundColor Gray

