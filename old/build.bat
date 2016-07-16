@echo off
set SOURCEDIR=%~dp0.
call %SOURCEDIR%\set_version.bat
call %SOURCEDIR%\set_dirs.bat %~1

IF NOT DEFINED PYEXE (EXIT)

set RELEASEDIR=%SOURCEDIR%\release
set VERSION=%RELEASE%_win%BITS%
set EXESTRING=ovpn_client_%VERSION%.exe

echo build %EXESTRING% ?
pause

if exist dist rmdir /S/Q dist\
if exist build rmdir /S/Q build\
if exist tmp rmdir /S/Q tmp\
if exist dist.7z del dist.7z
if exist %EXESTRING% del %EXESTRING%


%PYEXE% setup.py py2exe

call includes_to_dist.bat %~1

%EXE7Z% a -mx9 -t7z dist.7z dist\



echo Load file: '7zSFXcfg%BITS%.txt' into '7z SFX Builder', check [Edit Version Info = '%VERSION%'] + SFX Path = '%SOURCEDIR%\%EXESTRING%' and hit [Make SFX] !
pause
rmdir /S/Q dist\ build\
if exist dist.7z del dist.7z

REM exit
call release.bat
echo release.bat finished
pause
