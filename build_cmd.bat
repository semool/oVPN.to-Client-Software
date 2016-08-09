@echo off
set SOURCEDIR=%~dp0.

call %SOURCEDIR%\set_dirs.bat %~1

IF NOT DEFINED PYEXE (EXIT)

del "%SOURCEDIR%\*.pyc"
del "%SOURCEDIR%\*.pyo"

if exist %DISTDIR3% rmdir /S/Q %DISTDIR3%\
if exist %WORKPATH% rmdir /S/Q %WORKPATH%\

%PYEXE% -OO setup_cmd.py py2exe

echo py2exe compiled

copy includes\cacert_ovpn.pem %DISTDIR3%\cacert_ovpn.pem

if exist %WORKPATH% rmdir /S/Q %WORKPATH%\
pause
