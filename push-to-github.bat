@echo off
title Push KalaSetu to GitHub
cls
echo ================================================================
echo             Push KalaSetu to GitHub Repository
echo ================================================================
echo.
set /p REPO_URL="Enter your GitHub Repository URL (e.g. https://github.com/mrad11/kalasetu.git): "
if "%REPO_URL%"=="" (
    echo [!] No URL entered. Exiting.
    pause
    exit /b 1
)

echo.
echo Setting remote origin to: %REPO_URL%
git remote remove origin 2>nul
git remote add origin %REPO_URL%
git branch -M main

echo.
echo Pushing to GitHub main branch...
git push -u origin main

echo.
if %errorlevel% equ 0 (
    echo ================================================================
    echo [SUCCESS] Pushed to GitHub successfully!
    echo Now enable GitHub Pages in your repo:
    echo Settings -^> Pages -^> Build and deployment: Select 'GitHub Actions'
    echo ================================================================
) else (
    echo [!] Push encountered an error. Please check your URL and internet.
)
echo.
pause
