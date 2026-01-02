@echo off
title MusicSoundLevelUP - One-Click Deployment (Bento Edition)
color 0b

echo ========================================================
echo   🎵 MusicSoundLevelUP Deployment System
echo   🚀 Preparing to push Bento Edition v2.4 to GitHub...
echo ========================================================
echo.

:: 1. Add Changes
echo [1/3] Staging changes...
git add .
if %errorlevel% neq 0 (
    echo [ERROR] Failed to add files.
    pause
    exit /b
)

:: 2. Commit
echo [2/3] Committing changes...
git commit -m "Deploy Bento Edition v2.4 (Design & Docs)"
:: Ignore commit error if nothing to commit (e.g. already committed)
if %errorlevel% neq 0 (
    echo [INFO] No new changes to commit or commit failed. Proceeding to push...
)

:: 3. Push
echo [3/3] Pushing to GitHub (origin main)...
echo [INFO] If prompted for password/token, please enter it.
git push origin main

if %errorlevel% neq 0 (
    color 0c
    echo.
    echo [ERROR] Push failed!
    echo [TIP] Check your SSH keys or internet connection.
    echo.
) else (
    color 0a
    echo.
    echo [SUCCESS] Deployment Complete!
    echo The Bento Edition is now live on repository.
    echo.
)

pause
