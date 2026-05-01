@echo off
REM Tek tikla calistirilir hali. Cmd'den de cagirilabilir.
REM PowerShell scripti ExecutionPolicy bypass ile calistirir.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0eklentileri_kur.ps1"
echo.
pause
