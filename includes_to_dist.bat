@echo off
IF NOT DEFINED CERTUTIL (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT EXIST %CERTUTIL% (echo %CERTUTIL% NOT FOUND && PAUSE && EXIT)
IF NOT DEFINED INCLUDESDIR (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED DISTDIR (EXIT)
IF NOT DEFINED BITS (EXIT)

copy /Y "%INCLUDESDIR%\cacert_ovpn.pem" "%DISTDIR%\"
copy /Y "%SIGNTOOL%" "%DISTDIR%\"
xcopy /Y /E "%LOCALEDIR%" "%DISTDIR%\locale\"
xcopy /Y /E "%INCLUDESDIR%\themes" "%DISTDIR%\share\themes\"
copy /Y "else\app_icons\shield_exe_32px_32bpp.ico" "%DISTDIR%\share\icons\"

set GTKDLL32=libgtk-3-0.dll
set GTKDLL32PX=libgtk-3-0-32.dll
set GTKDLLFILE=%DLLDIR_U%\%GTKDLL32PX%

IF EXIST %DLLDIR_U%\%GTKDLL32% (
	setlocal EnableDelayedExpansion
	set /a COUNTER=1
	for /F "tokens=* delims=" %%D in ('"%CERTUTIL% -hashfile %DISTDIR%\%GTKDLL32% sha1"') do (
		IF !COUNTER! EQU 2 set "SHA1_DIST=%%D"
		set /a COUNTER+=1
	)
	echo !SHA1_DIST: =!
	set /a COUNTER=1
	for /F "tokens=* delims=" %%D in ('"%CERTUTIL% -hashfile %DLLDIR_U%\%GTKDLL32% sha1"') do (
		IF !COUNTER! EQU 2 set "SHA1_U=%%D"
		set /a COUNTER+=1
	)
	echo !SHA1_U: =!
	IF "!SHA1_DIST: =!" NEQ "!SHA1_U: =!" (
		echo SHA1 check Failed, delete old %GTKDLL32% and %GTKDLL32PX%
		del "%DLLDIR_U%\%GTKDLL32%" 2> nul
		del "%DLLDIR_S%\%GTKDLL32%" 2> nul
		del "%DLLDIR_U%\%GTKDLL32PX%" 2> nul
		del "%DLLDIR_S%\%GTKDLL32PX%" 2> nul
	)
	endlocal
)

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
