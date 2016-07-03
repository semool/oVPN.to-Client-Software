echo off
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
if exist dist.7z del dist.7z
if exist %EXESTRING% del %EXESTRING%


copy /Y "%INCLUDESDIR%\ico\292.ico" "%SOURCEDIR%"
%PYEXE% setup.py py2exe
del 292.ico

xcopy /Y /E "%INCLUDESDIR%\ico" "%DISTDIR%\ico\"
xcopy /Y /E "%INCLUDESDIR%\dns" "%DISTDIR%\dns\"
xcopy /Y /E "%INCLUDESDIR%\MS-Windows" "%DISTDIR%\share\themes\MS-Windows\"
copy /Y "%INCLUDESDIR%\cacert_ovpn.pem" "%DISTDIR%\"

copy /Y "%INCLUDESDIR%\crypt32_win%BITS%.dll" "dist\crypt32.dll"

%EXE7Z% a -mx9 -t7z dist.7z dist\

rmdir /S/Q dist\ build\

echo Load file: '7zSFXcfg%BITS%.txt' into '7z SFX Builder', check [Edit Version Info = '%VERSION%'] + SFX Path = '%SOURCEDIR%\%EXESTRING%' and hit [Make SFX] !
pause
if exist dist.7z del dist.7z

REM exit
call release.bat
echo release.bat finished
pause