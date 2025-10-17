@echo off
echo ========================================
echo  Installing Gettext Tools
echo ========================================
echo.

REM Download gettext installer
echo Downloading gettext installer...
powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/mlocati/gettext-iconv-windows/releases/download/v0.21-v1.16/gettext0.21-iconv1.16-static-64.exe' -OutFile '%TEMP%\gettext-installer.exe'}"

if exist "%TEMP%\gettext-installer.exe" (
    echo.
    echo Running installer...
    echo Please follow the installation wizard.
    echo.
    start /wait %TEMP%\gettext-installer.exe
    
    echo.
    echo ========================================
    echo  Installation Complete!
    echo ========================================
    echo.
    echo Please RESTART your terminal/command prompt
    echo Then run: msgfmt --version
    echo.
    del "%TEMP%\gettext-installer.exe"
) else (
    echo.
    echo Download failed. Please download manually from:
    echo https://github.com/mlocati/gettext-iconv-windows/releases
    echo.
)

pause
