$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath('Desktop')
$ShortcutPath = Join-Path $DesktopPath "KalaSetu AI.lnk"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$HtmlPath = Join-Path $ScriptDir "index.html"
$IconPath = Join-Path $ScriptDir "kalasetu-icon.ico"

$TargetExe = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $TargetExe)) {
    $TargetExe = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}
if (-not (Test-Path $TargetExe)) {
    $TargetExe = "C:\Program Files\Google\Chrome\Application\chrome.exe"
}
if (-not (Test-Path $TargetExe)) {
    $TargetExe = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
}

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
if (Test-Path $TargetExe) {
    $Shortcut.TargetPath = $TargetExe
    $formattedUrl = "file:///" + $HtmlPath.Replace('\', '/')
    $Shortcut.Arguments = "--app=`"$formattedUrl`" --window-size=1280,820"
} else {
    $Shortcut.TargetPath = $HtmlPath
}

$Shortcut.WorkingDirectory = $ScriptDir
if (Test-Path $IconPath) {
    $Shortcut.IconLocation = "$IconPath,0"
}
$Shortcut.Description = "KalaSetu AI - Smart Cataloging and Market Linkage"
$Shortcut.Save()

if (Test-Path $ShortcutPath) {
    Write-Host "`n[SUCCESS] KalaSetu AI Desktop shortcut created at: $ShortcutPath" -ForegroundColor Green
} else {
    Write-Host "`n[ERROR] Failed to create shortcut." -ForegroundColor Red
}
