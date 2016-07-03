@echo off
set PY32=C:\Python27
set PY64=C:\Python27_64

set APPDIR=%APPDATA%\ovpn\bin\client\dist
set EXE7Z="%PROGRAMFILES%\7-Zip\7z.exe"

REM DONT CHANGE DOWN HERE !

set BITS=%~1
set PY32EXE=%PY32%\python.exe
set PY64EXE=%PY64%\python.exe
IF "%~1" == "32" (set PYEXE=%PY32EXE%)
IF "%~1" == "64" (set PYEXE=%PY64EXE%)
IF NOT DEFINED PYEXE (echo "MISSING BITS" && PAUSE && EXIT)
IF NOT EXIST %PYEXE% (echo PYEXE %PYEXE% NOT FOUND && PAUSE && EXIT)

set INCLUDESDIR=%SOURCEDIR%\includes
set DISTDIR=%SOURCEDIR%\dist

echo dir vars loaded
echo %SOURCEDIR%
