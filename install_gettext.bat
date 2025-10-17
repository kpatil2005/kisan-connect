@echo off
echo ========================================
echo  Installing Gettext Tools
echo ========================================
echo.

REM Check if Chocolatey is installed
where choco >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Chocolatey found! Installing gettext...
    choco install gettext -y
    echo.
    echo ========================================
    echo  Gettext installed successfully!
    echo ========================================
    goto :end
)

echo Chocolatey not found. Installing Chocolatey first...
echo.
echo Please run this command in PowerShell as Administrator:
echo.
echo Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
echo.
echo After installing Chocolatey, run this batch file again.
echo.
echo ========================================
echo  Alternative: Manual Download
echo ========================================
echo.
echo Download from: https://mlocati.github.io/articles/gettext-iconv-windows.html
echo Choose: gettext0.21-iconv1.16-static-64.exe
echo.

:end
pause
