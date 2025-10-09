@echo off
echo Starting Django Development Server...
echo.

REM Activate virtual environment if it exists
if exist "env\Scripts\activate.bat" (
    call env\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo No virtual environment found, using system Python
)

echo.
echo Running migrations...
python manage.py migrate

echo.
echo Starting server at http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver

pause
