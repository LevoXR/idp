# PowerShell script to help setup network access for Aditya Setu
# This script shows your IP address and provides instructions for firewall configuration

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Aditya Setu - Network Access Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get local IP address
Write-Host "Finding your local IP address..." -ForegroundColor Yellow
try {
    $ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {
        $_.IPAddress -notlike "127.*" -and 
        $_.IPAddress -notlike "169.254.*"
    } | Select-Object -First 1).IPAddress
    
    if ($ipAddress) {
        Write-Host "Your IP address: $ipAddress" -ForegroundColor Green
        Write-Host ""
        Write-Host "Server will be accessible at:" -ForegroundColor Yellow
        Write-Host "  - Local: http://localhost:8000" -ForegroundColor White
        Write-Host "  - Network: http://$ipAddress:8000" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host "Could not automatically detect IP address." -ForegroundColor Yellow
        Write-Host "Run 'ipconfig' to find your IPv4 address manually." -ForegroundColor Yellow
    }
} catch {
    Write-Host "Error detecting IP address: $_" -ForegroundColor Red
    Write-Host "Run 'ipconfig' to find your IPv4 address manually." -ForegroundColor Yellow
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Firewall Configuration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To allow access from other devices, you need to configure Windows Firewall." -ForegroundColor Yellow
Write-Host ""
Write-Host "Option 1: Automatic (Run as Administrator)" -ForegroundColor Cyan
Write-Host "  This script can add a firewall rule automatically." -ForegroundColor White
Write-Host ""
Write-Host "Option 2: Manual" -ForegroundColor Cyan
Write-Host "  1. Open Windows Defender Firewall" -ForegroundColor White
Write-Host "  2. Click 'Advanced settings'" -ForegroundColor White
Write-Host "  3. Click 'Inbound Rules' → 'New Rule'" -ForegroundColor White
Write-Host "  4. Select 'Port' → Next" -ForegroundColor White
Write-Host "  5. Select 'TCP' and enter port 8000" -ForegroundColor White
Write-Host "  6. Allow the connection" -ForegroundColor White
Write-Host "  7. Apply to all profiles" -ForegroundColor White
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if ($isAdmin) {
    Write-Host "Running as Administrator. Would you like to add a firewall rule automatically? (Y/N)" -ForegroundColor Yellow
    $response = Read-Host
    
    if ($response -eq "Y" -or $response -eq "y") {
        try {
            Write-Host "Adding firewall rule for port 8000..." -ForegroundColor Yellow
            New-NetFirewallRule -DisplayName "Aditya Setu - Port 8000" `
                -Direction Inbound `
                -LocalPort 8000 `
                -Protocol TCP `
                -Action Allow `
                -Description "Allow incoming connections for Aditya Setu web server" | Out-Null
            
            Write-Host "Firewall rule added successfully!" -ForegroundColor Green
        } catch {
            Write-Host "Error adding firewall rule: $_" -ForegroundColor Red
            Write-Host "Please configure the firewall manually using the instructions above." -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "Note: To add firewall rule automatically, run this script as Administrator." -ForegroundColor Yellow
    Write-Host "Right-click PowerShell and select 'Run as Administrator', then run this script again." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next Steps" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Make sure the firewall is configured (see above)" -ForegroundColor White
Write-Host "2. Run the server: python run.py" -ForegroundColor White
Write-Host "3. Access from other devices using: http://$ipAddress:8000" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")




