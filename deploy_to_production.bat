@echo off
echo ========================================
echo   DEPLOYING TO PRODUCTION (GitHub)
echo ========================================
echo.

REM Navigate to project directory
cd /d "%~dp0"

echo Step 1: Checking Git status...
git status
echo.

echo Step 2: Adding all changes...
git add .
echo.

echo Step 3: Committing changes...
set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg="Mobile responsive fixes and UI improvements"
git commit -m "%commit_msg%"
echo.

echo Step 4: Pushing to GitHub...
git push origin main
echo.

echo ========================================
echo   DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Your changes have been pushed to GitHub.
echo.
echo NEXT STEPS FOR RENDER DEPLOYMENT:
echo 1. Go to https://dashboard.render.com
echo 2. Find your service (kisan-connect)
echo 3. Click "Manual Deploy" -> "Deploy latest commit"
echo 4. Wait 5-10 minutes for deployment
echo 5. Visit: https://kisan-connect.onrender.com
echo.
echo ========================================

pause
