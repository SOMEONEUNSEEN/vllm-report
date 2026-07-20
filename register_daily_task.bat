@echo off
chcp 65001 >nul
echo ========================================
echo  Register Daily Refresh Task
echo ========================================
echo.

set "TASK_NAME=vLLM Dashboard Daily Refresh"
set "SCRIPT_PATH=%~dp0daily_refresh.bat"

echo Task Name: %TASK_NAME%
echo Script Path: %SCRIPT_PATH%
echo.

schtasks /Create /TN "%TASK_NAME%" /TR "\"%SCRIPT_PATH%\"" /SC DAILY /ST 09:00 /RL HIGHEST /F

if %errorlevel% equ 0 (
    echo.
    echo Task registered successfully!
    echo It will run daily at 09:00 AM.
) else (
    echo.
    echo Failed to register task.
    echo Please run this script as Administrator.
)

echo.
pause
