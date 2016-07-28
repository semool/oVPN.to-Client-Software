@echo off
set SOURCEDIR=%~dp0.

call %SOURCEDIR%\set_dirs.bat %~1

IF NOT DEFINED PYEXE (EXIT)

del "%SOURCEDIR%\*.pyc"
del "%SOURCEDIR%\*.pyo"

%PYEXE% release_version.py SET_VERSION_FILES

call %SOURCEDIR%\set_version.bat

set RELEASEDIR=%SOURCEDIR%\release
set VERSION=v%RELEASE%-gtk3_win%BITS%
set EXESTRING=ovpn_client_%VERSION%_setup.exe
::set EXESTRING="oVPN.to-Client-%VERSION%-setup.exe"

echo cleanup before building
if exist %DISTDIR% rmdir /S/Q %DISTDIR%\
if exist %WORKPATH% rmdir /S/Q %WORKPATH%\
if exist %EXESTRING% del %EXESTRING%

%PYEXE% -OO setup.py py2exe
echo py2exe compiled, hit to call includes_to_dist.bat %~1
pause

call includes_to_dist.bat %~1
echo includes_to_dist.bat completed

IF "%~2" == "SIGN" (
	echo hit to SIGN files in %DISTDIR%
	for %%v in (%DISTDIR%\*.exe) do (
		echo sign?: %%v
	)
	pause
	call sign_exe.bat
	)

echo hit to compile: inno_setup%BITS%.iss
pause
%INNOCOMPILE% /cc "%SOURCEDIR%\inno_setup%BITS%.iss"

echo Inno Setup %EXESTRING%
echo Close or hit to make release
pause

call release.bat
echo release.bat finished, close or hit to cleanup
pause

if exist %DISTDIR% rmdir /S/Q %DISTDIR%\
if exist %WORKPATH% rmdir /S/Q %WORKPATH%\