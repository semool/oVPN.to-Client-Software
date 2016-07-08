@echo off
set SOURCEDIR=%~dp0.
call %SOURCEDIR%\set_version.bat
call %SOURCEDIR%\set_dirs.bat %~1

IF NOT DEFINED PYEXE (EXIT)

set RELEASEDIR=%SOURCEDIR%\release
set VERSION=%RELEASE%_win%BITS%
set EXESTRING=ovpn_client_%VERSION%_inno.exe

echo build %EXESTRING% ?
pause

if exist dist rmdir /S/Q dist\
if exist build rmdir /S/Q build\
if exist dist.7z del dist.7z
if exist %EXESTRING% del %EXESTRING%


%PYEXE% setup.py py2exe

call includes_to_dist.bat %~1

echo Run inno_setup%BITS%.iss now
pause
rmdir /S/Q dist\ build\

REM exit
call release.bat
echo release.bat finished
pause
