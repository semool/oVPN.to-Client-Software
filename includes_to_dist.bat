@echo off
IF NOT DEFINED INCLUDESDIR (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED DISTDIR (EXIT)
IF NOT DEFINED BITS (EXIT)

copy /Y "%INCLUDESDIR%\cacert_ovpn.pem" "%DISTDIR%\"
xcopy /Y /E "%LOCALEDIR%" "%DISTDIR%\locale\"
xcopy /Y /E "%INCLUDESDIR%\themes" "%DISTDIR%\share\themes\"
copy /Y "%INCLUDESDIR%\libgtk3-tray32\libgtk-3-0-32_win%BITS%.dll" "%DISTDIR%\libgtk-3-0-32.dll"

::Delete unneded Language Files 
for /f "delims=" %%i in ('dir /b "%LANGPATH%*.*"') do (
    IF NOT "%%i" == "de" IF NOT "%%i" == "en" IF NOT "%%i" == "es" (
        rd /s /q "%LANGPATH%%%i" 2>nul
    )
)

mkdir "%DISTDIR%\appdata"
echo %RELEASE% > "%DISTDIR%\appdata\version