@echo off
set SOURCEDIR=%~dp0.

call %SOURCEDIR%\set_dirs.bat %~1

IF NOT DEFINED PYEXE (EXIT)

del "%SOURCEDIR%\*.pyc"
del "%SOURCEDIR%\*.pyo"

set DISTPATH=%SOURCEDIR%\dist_check_bin
::set WORKPATH=%SOURCEDIR%\work_check_bin
set WORKPATH=%SOURCEDIR%\build

if exist %DISTPATH% rmdir /S/Q %DISTPATH%\
if exist %WORKPATH% rmdir /S/Q %WORKPATH%\

%PYEXE% -OO setup_check_bin.py py2exe

::%PYINSTALLER% --uac-admin --clean --distpath "%DISTPATH%" --workpath "%$WORKPATH%" %SOURCEDIR%\check_bin.spec 
::%PYINSTALLER% -d -D --uac-admin --clean --distpath "%DISTPATH%" %SOURCEDIR%\check_bin.spec 
::%PYINSTALLER% -d -F --windowed --uac-admin --clean --distpath "%DISTPATH%" %SOURCEDIR%\check_bin.spec 



if exist %DISTPATH% del %DISTPATH%\check_bin\*.pyd
::if exist %WORKPATH% rmdir /S/Q %WORKPATH%

echo check_bin compiled
pause
