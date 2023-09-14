@echo off
chcp 65001 > nul
cls

echo ╔═╗┌─┐┌┬┐┬ ┬┌─┐
echo ╚═╗├┤  │ │ │├─┘
echo ╚═╝└─┘ ┴ └─┘┴  
echo ===================
echo.

:: Lista de bibliotecas requeridas
set "required_libraries=ctypes aiohttp asyncio discord_webhook colorama msvcrt"

echo Instalando bibliotecas requeridas...
for %%i in (%required_libraries%) do (
    pip install %%i >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] No se pudo instalar %%i.
    ) else (
        echo [INFO] %%i ha sido instalado con éxito.
    )
)

echo.
echo [INFO] Todas las bibliotecas han sido instaladas con éxito.
pause
