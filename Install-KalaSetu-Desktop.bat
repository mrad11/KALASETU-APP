@echo off
setlocal
title Installing KalaSetu AI Desktop App

echo =======================================================
echo          KalaSetu AI - Desktop App Installer
echo =======================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0create_shortcut.ps1"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo =======================================================
    echo  Look on your Windows Desktop for "KalaSetu AI".
    echo =======================================================
    echo.
    set /p LAUNCH="Would you like to launch KalaSetu AI now? (Y/N): "
    if /i "%LAUNCH%"=="Y" (
        powershell -NoProfile -Command "Start-Process ([System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'KalaSetu AI.lnk'))"
    )
) else (
    echo.
    echo [ERROR] Could not create desktop shortcut.
)

echo.
pause
