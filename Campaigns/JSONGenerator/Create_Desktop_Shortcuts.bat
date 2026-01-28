@echo off
REM Creates desktop shortcuts for easy access to the extractor

echo ========================================
echo Creating Desktop Shortcuts
echo ========================================
echo.

set SCRIPT_DIR=%~dp0
set DESKTOP=%USERPROFILE%\Desktop

REM Create shortcut for GUI version
echo Creating shortcut: Campaign Extractor (GUI)...
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%DESKTOP%\Campaign Extractor.lnk');$s.TargetPath='%SCRIPT_DIR%Extract_Campaign_Content_GUI.bat';$s.WorkingDirectory='%SCRIPT_DIR%';$s.Description='Extract campaign content from Word docs';$s.Save()"

if exist "%DESKTOP%\Campaign Extractor.lnk" (
    echo [SUCCESS] Shortcut created on desktop!
    echo.
    echo You can now double-click "Campaign Extractor" on your desktop
    echo to extract content from Word documents.
) else (
    echo [ERROR] Could not create shortcut
)

echo.
echo Press any key to close...
pause >nul

