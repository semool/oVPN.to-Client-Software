@echo off
set PY32=C:\Python27
set PY64=C:\Python27_64

set APPDIR=%APPDATA%\ovpn\bin\client\dist
set EXE7Z="%PROGRAMFILES%\7-Zip\7z.exe"
set SIGNTOOL="E:\codesign\signtool_w7sdk.exe"

REM DONT CHANGE DOWN HERE !

set BITS=%~1
set PY32EXE=%PY32%\python.exe
set PY64EXE=%PY64%\python.exe
set PY32GET=%PY32%\Tools\i18n
set PY64GET=%PY64%\Tools\i18n

IF "%BITS%" == "32" (
	set PYEXE=%PY32EXE%
	set PYGET=%PY32GET%
)

IF "%BITS%" == "64" (
	set PYEXE=%PY64EXE%
	set PYGET=%PY64GET%
)

IF NOT DEFINED PYEXE (echo "MISSING BITS" && PAUSE && EXIT)
IF NOT EXIST %PYEXE% (echo PYEXE %PYEXE% NOT FOUND && PAUSE && EXIT)

set INCLUDESDIR=%SOURCEDIR%\includes
set LOCALEDIR=%SOURCEDIR%\locale
set DISTDIR=%SOURCEDIR%\dist
set LANGPATH=%SOURCEDIR%\dist\share\locale\
set INNOCOMPILE="C:\Program Files (x86)\Inno Setup 5\Compil32.exe"

echo dir vars loaded
echo %SOURCEDIR%
