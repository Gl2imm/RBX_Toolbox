@echo off
setlocal enabledelayedexpansion

set "START_DIR=%cd%"
set "DELETE_DEP_PUBLIC=false"

REM Ask once if user wants to delete dependencies_public folders
set /p "CHOICE=Do you want to delete all 'dependencies_public' folders? (Y/N): "
if /i "%CHOICE%"=="Y" (
    set "DELETE_DEP_PUBLIC=true"
)

REM Delete all __pycache__ folders (case-insensitive, recursive)
for /f "delims=" %%F in ('dir /b /s /ad ^| findstr /i /r "\\__pycache__$"') do (
    rd /s /q "%%F" 2>nul
)

REM Conditionally delete dependencies_public folders
if "%DELETE_DEP_PUBLIC%"=="true" (
    for /f "delims=" %%F in ('dir /b /s /ad ^| findstr /i /r "\\dependencies_public$"') do (
        rd /s /q "%%F" 2>nul
    )
)

endlocal
exit
