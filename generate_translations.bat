@echo off
echo ========================================
echo  Generating Translation Files
echo ========================================
echo.

cd /d "%~dp0"

echo Creating locale directory...
if not exist "locale" mkdir locale

echo.
echo Generating translation files for all languages...
python manage.py makemessages -l hi -l ta -l te -l bn -l mr -l kn -l ml -l pa --ignore=venv --ignore=env

echo.
echo ========================================
echo  Translation files created successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .po files in locale/[language]/LC_MESSAGES/django.po
echo 2. Add translations for each msgid
echo 3. Run: python manage.py compilemessages
echo.
pause
