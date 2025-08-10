@echo off
echo ===================================
echo Facebook Reels Bot Setup (Enhanced)
echo ===================================
echo.

echo Checking for Python installation...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or newer from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Python is installed. Installing required packages...
echo.

echo Installing core dependencies...
pip install selenium webdriver-manager pywinauto pyautogui pyperclip

echo.
echo Installing undetected Chrome driver for bot detection avoidance...
pip install undetected-chromedriver

echo.
echo Installing additional requirements if requirements.txt exists...
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo No requirements.txt found, skipping...
)

if %errorlevel% neq 0 (
    echo.
    echo Some packages may have failed to install.
    echo The bot should still work with basic functionality.
    echo Check the error messages above for details.
    echo.
)

echo.
echo ===================================
echo Setup completed successfully!
echo.
echo NEW FEATURES INSTALLED:
echo - Undetected Chrome (avoids bot detection)
echo - Multi-page support
echo - Enhanced element detection
echo - Chrome focus protection
echo.
echo BEFORE RUNNING THE BOT:
echo 1. Make sure Chrome browser is installed
echo 2. Edit run_bot.py to configure:
echo    - FACEBOOK_EMAIL and FACEBOOK_PASSWORD
echo    - FOLDER_PAGE_CONFIGS array with your pages and video folders
echo 3. Choose execution mode when running:
echo    - Multi-Page Mode: Processes all configured pages
echo    - Single Page Mode: Legacy single page processing
echo.
echo RUN THE BOT WITH:
echo    python run_bot.py
echo.
echo TROUBLESHOOTING:
echo - If undetected Chrome fails, bot will fallback to regular Chrome
echo - Check README.md for detailed configuration instructions
echo - Debug screenshots are saved automatically for troubleshooting
echo ===================================
echo.
pause