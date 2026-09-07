@echo off
rem Abre o assistente de curadoria do catalogo dadosrgb.
rem Roda com pythonw para nao deixar janela preta de console aberta.

set "APP=%~dp0curadoria\curadoria.pyw"

if not exist "%APP%" (
  echo Nao encontrei o assistente em:
  echo   %APP%
  echo.
  pause
  exit /b 1
)

where pythonw >nul 2>&1
if %errorlevel%==0 (
  start "" pythonw "%APP%"
  exit /b 0
)

where py >nul 2>&1
if %errorlevel%==0 (
  start "" py -3 "%APP%"
  exit /b 0
)

echo Python nao foi encontrado no PATH.
echo Instale em https://python.org e marque "Add Python to PATH".
echo.
pause
exit /b 1
