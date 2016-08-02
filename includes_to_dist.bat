@echo off
IF NOT DEFINED INCLUDESDIR (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED DISTDIR (EXIT)
IF NOT DEFINED BITS (EXIT)

copy /Y "%INCLUDESDIR%\cacert_ovpn.pem" "%DISTDIR%\"
xcopy /Y /E "%LOCALEDIR%" "%DISTDIR%\locale\"
xcopy /Y /E "%INCLUDESDIR%\themes" "%DISTDIR%\share\themes\"

set GTKDLL32PX=libgtk-3-0-32.dll
set GTKDLLFILE=%DLLDIR_U%\%GTKDLL32PX%
IF NOT EXIST %GTKDLLFILE% (
	call patch_gtkdll.bat %~1
	echo copy /Y %GTKDLLFILE% %DISTDIR%\%GTKDLL32PX%
	copy /Y %GTKDLLFILE% %DISTDIR%\%GTKDLL32PX%
) ELSE (
	echo copy /Y %GTKDLLFILE% %DISTDIR%\%GTKDLL32PX%
	copy /Y %GTKDLLFILE% %DISTDIR%\%GTKDLL32PX%
)



::Delete unneded Language Files 
for /f "delims=" %%i in ('dir /b "%LANGPATH%*.*"') do (
	IF NOT "%%i" == "de" IF NOT "%%i" == "en" IF NOT "%%i" == "es" (
		rd /s /q "%LANGPATH%%%i" 2>nul
	)
)

mkdir "%DISTDIR%\appdata"
echo %RELEASE% > "%DISTDIR%\appdata\version