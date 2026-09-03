@echo off
title KalaSetu AI - Mobile and Desktop App Server
cd /d "%~dp0"

echo ==========================================================
echo       Starting KalaSetu AI Local Network Server
echo ==========================================================
echo.

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python was not found in PATH.
    echo Please make sure Python is installed to run the local server.
    pause
    exit /b 1
)

python serve.py

pause
