# Install Gettext Tools for Translation

## Problem
Django i18n requires GNU gettext tools to compile translations.

## Solution - Install Gettext

### Option 1: Using Chocolatey (Recommended)
```bash
# Install Chocolatey first (if not installed)
# Run PowerShell as Administrator and paste:
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Then install gettext
choco install gettext
```

### Option 2: Manual Download
1. Download from: https://mlocati.github.io/articles/gettext-iconv-windows.html
2. Download the "static" version (gettext0.21-iconv1.16-static-64.exe)
3. Run the installer
4. Add to PATH: `C:\Program Files\gettext-iconv\bin`

### Option 3: Using Git Bash (if you have Git installed)
Git for Windows includes gettext tools.
Add to PATH: `C:\Program Files\Git\usr\bin`

## After Installation

Restart your terminal and run:
```bash
# Generate translation files
python manage.py makemessages -l hi

# Compile translations
python manage.py compilemessages
```

## Quick Test Without Gettext

For now, I've created a manual workaround. Follow these steps:

1. I've already created the Hindi translation file
2. Use the Python script below to compile it manually
