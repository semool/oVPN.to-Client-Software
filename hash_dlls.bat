@echo off
set SOURCEDIR=%~dp0.
call %SOURCEDIR%\set_dirs.bat %~1

echo run hash_dlls on %BITS% bits
echo PYEXE=%PYEXE%
REM pause

%PYEXE% %SOURCEDIR%\hash_dlls.py %~1

echo "hit to quit"
pause
