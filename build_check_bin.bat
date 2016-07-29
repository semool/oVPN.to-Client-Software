@echo off
set SOURCEDIR=%~dp0.

call %SOURCEDIR%\set_dirs.bat %~1

IF NOT DEFINED PYEXE (EXIT)

del "%SOURCEDIR%\*.pyc"
del "%SOURCEDIR%\*.pyo"

set DISTPATH=%DISTDIR2%

if exist %DISTDIR2% rmdir /S/Q %DISTDIR2%\
if exist %WORKPATH% rmdir /S/Q %WORKPATH%\

%PYEXE% -OO setup_check_bin.py py2exe

echo py2exe compiled check_bin 

if exist %WORKPATH% rmdir /S/Q %WORKPATH%\
pause
