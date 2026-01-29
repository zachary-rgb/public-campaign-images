@echo off
REM Simple batch file to run the campaign content extractor
REM Just double-click this file to extract content from Word docs!

echo ========================================
echo Campaign Content Extractor
echo ========================================
echo.

cd /d "%~dp0"

python extract_to_google_sheets.py

echo.
echo Press any key to close...
pause >nul

