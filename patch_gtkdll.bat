@echo off
set SOURCEDIR=%~dp0.
call %SOURCEDIR%\set_dirs.bat %~1

echo run patch_gtkdll on %BITS% bits
echo PYEXE=%PYEXE%
REM pause

%PYEXE% %SOURCEDIR%\patch_gtkdll.py %~1

echo "hit to quit"
pause
