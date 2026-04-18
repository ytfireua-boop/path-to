@echo off
:menu
cls
echo ========================================
echo        path-to PATH Manager
echo ========================================
echo.
echo 1. Install path-to to PATH
echo 2. Uninstall path-to from PATH
echo 3. Exit
echo.
set /p choice="Please select an option (1-3): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto uninstall
if "%choice%"=="3" goto exit
echo Invalid choice. Please try again.
pause
goto menu

:install
cls
echo Installing path-to.exe to system PATH...

REM Get current directory
set "CURRENT_DIR=%~dp0"
REM Remove trailing backslash
set "CURRENT_DIR=%CURRENT_DIR:~0,-1%"

REM Add executable folder to PATH
set "EXECUTABLE_DIR=%CURRENT_DIR%executable"
echo Adding %EXECUTABLE_DIR% to PATH...
setx PATH "%PATH%;%EXECUTABLE_DIR%" >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo.
    echo SUCCESS: path-to.exe has been added to your PATH!
    echo.
    echo You can now use 'path-to' from any directory.
    echo.
    echo NOTE: You may need to restart your command prompt or restart your computer
    echo       for changes to take effect.
    echo.
    echo To test: path-to --help
) else (
    echo.
    echo ERROR: Failed to add to PATH.
    echo.
    echo Please try running this script as Administrator.
)

echo.
pause
goto menu

:uninstall
cls
echo Uninstalling path-to.exe from system PATH...

REM Get current directory
set "CURRENT_DIR=%~dp0"
REM Remove trailing backslash
set "CURRENT_DIR=%CURRENT_DIR:~0,-1%"
set "EXECUTABLE_DIR=%CURRENT_DIR%executable"

echo.
echo WARNING: This will remove path-to from your system PATH!
echo.
echo About to remove: %EXECUTABLE_DIR%
echo.
set /p confirm="Are you sure you want to continue? (y/n): "

if /i "%confirm%" NEQ "y" (
    echo.
    echo Uninstall cancelled by user.
    echo.
    pause
    goto menu
)

REM Remove executable folder from PATH
echo Removing %EXECUTABLE_DIR% from PATH...
set "NEW_PATH=%PATH%"
set "NEW_PATH=!NEW_PATH:%EXECUTABLE_DIR%=!"
setx PATH "%NEW_PATH%" >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo.
    echo SUCCESS: path-to.exe has been removed from your PATH!
    echo.
    echo You will no longer be able to use 'path-to' from any directory.
    echo.
    echo NOTE: You may need to restart your command prompt or restart your computer
    echo       for changes to take effect.
) else (
    echo.
    echo ERROR: Failed to remove from PATH.
    echo.
    echo Please try running this script as Administrator.
)

echo.
pause
goto menu

:exit
cls
echo Goodbye!
echo.
pause
