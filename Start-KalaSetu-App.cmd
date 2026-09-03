@echo off
set "HTML_PATH=%~dp0index.html"

if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --app="file:///%HTML_PATH:\=/%" --window-size=1280,820
) else if exist "C:\Program Files\Microsoft\Edge\Application\msedge.exe" (
    start "" "C:\Program Files\Microsoft\Edge\Application\msedge.exe" --app="file:///%HTML_PATH:\=/%" --window-size=1280,820
) else if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --app="file:///%HTML_PATH:\=/%" --window-size=1280,820
) else (
    start "" "%HTML_PATH%"
)
