@echo off
set SOURCEDIR=%~dp0.
call %SOURCEDIR%\set_version.bat
call %SOURCEDIR%\set_dirs.bat %~1

IF NOT DEFINED PYEXE (EXIT)

set RELEASEDIR=%SOURCEDIR%\release
set VERSION=v%RELEASE%-gtk3_win%BITS%
set EXESTRING=ovpn_client_%VERSION%_setup.exe
::set EXESTRING="oVPN.to-Client-%VERSION%-setup.exe"

echo build %EXESTRING% ?
pause

if exist dist rmdir /S/Q dist\
if exist build rmdir /S/Q build\
if exist dist.7z del dist.7z
if exist %EXESTRING% del %EXESTRING%


%PYEXE% setup.py py2exe
pause

call includes_to_dist.bat %~1

echo Run inno_setup%BITS%.iss now?
pause

%INNOCOMPILE% /cc "%SOURCEDIR%\inno_setup%BITS%.iss"
rmdir /S/Q dist\ build\

echo Compiled %EXESTRING%
pause
REM exit
call release.bat
echo release.bat finished
pause
