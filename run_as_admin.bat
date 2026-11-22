@echo off
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Запуск программы...
    python remove_shortcut_arrow.py
) else (
    echo Запрос прав администратора...
    powershell -Command "Start-Process python -ArgumentList 'remove_shortcut_arrow.py' -Verb RunAs"
)
pause