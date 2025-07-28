@echo off
echo ===================================
echo Facebook Reels Bot Setup
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
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo Failed to install required packages.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo ===================================
echo Setup completed successfully!
echo.
echo Before running the bot:
echo 1. Make sure Chrome browser is installed
echo 2. Edit run_bot.py to update your Facebook credentials and video folder path
echo 3. Run the bot with: python run_bot.py
echo ===================================
echo.
pause