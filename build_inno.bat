@echo off
set SOURCEDIR=%~dp0.

call %SOURCEDIR%\set_dirs.bat %~1

IF NOT DEFINED PYEXE (EXIT)

del "%SOURCEDIR%\*.pyc" 2> nul
del "%SOURCEDIR%\*.pyo" 2> nul

%PYEXE% release_version.py SET_VERSION_FILES

call %SOURCEDIR%\set_version.bat

set RELEASEDIR=%SOURCEDIR%\release
set VERSION=v%RELEASE%-gtk3_win%BITS%
set EXESTRING=ovpn_client_%VERSION%_setup.exe
::set EXESTRING="oVPN.to-Client-%VERSION%-setup.exe"

echo cleanup
IF EXIST %DISTDIR% rmdir /S/Q %DISTDIR%\
IF EXIST %WORKPATH% rmdir /S/Q %WORKPATH%\
IF EXIST %EXESTRING% del %EXESTRING%
IF EXIST %PY2EXE_ERR% del %PY2EXE_ERR%
IF EXIST %PY2EXE_LOG% del %PY2EXE_LOG%
IF EXIST %SOURCEDIR%\client_debug.log del %SOURCEDIR%\client_debug.log
IF EXIST inno_setup.iss del inno_setup.iss

::echo hit to compile py2exe: %BINARY%
::pause
echo compiling py2exe...
%PYEXE% -OO setup.py py2exe 1> %PY2EXE_LOG% 2> %PY2EXE_ERR%
IF NOT %errorlevel% == 0 (
	echo py2exe compiled with exitcode %errorlevel%: logfile: %PY2EXE_LOG%
	for %%F in (%SOURCEDIR%\py2exe*.log) do if %%~zF equ 0 del %%F
	IF EXIST %PY2EXE_ERR% notepad.exe %PY2EXE_ERR%
	::pause
	exit
	)


::echo py2exe completed
::echo Close or hit to continue with includes_to_dist
::pause

call includes_to_dist.bat %~1
set INCLUDESRETURN=%errorlevel%
echo includes return %INCLUDESRETURN%

echo cleanup
if exist %WORKPATH% rmdir /S/Q %WORKPATH%\
if exist %SOURCEDIR%\tmp\ rmdir /S/Q %SOURCEDIR%\tmp\
IF EXIST %PY2EXE_LOG% del %PY2EXE_LOG%
IF EXIST %PY2EXE_ERR% del %PY2EXE_ERR%
rmdir /S/Q %PYCACHE%\
del "%SOURCEDIR%\*.pyc" 2> nul
del "%SOURCEDIR%\*.pyo" 2> nul

IF NOT %INCLUDESRETURN% == 0 (
	echo includes_to_dist.bat failed code %errorlevel%
	pause
	exit
	)
	
echo includes_to_dist.bat completed


IF NOT "%~2" == "SIGN" (
	echo SIGN ARGUMENT MISSING
	pause
	exit
	)

IF "%~2" == "SIGN" (
	call sign_exe.bat
	call sign_dll.bat
	)

echo launch %INNOCOMPILE%
%INNOCOMPILE% /cc "%SOURCEDIR%\inno_setup.iss"
set INNORETURN=%errorlevel%

echo Inno Setup %EXESTRING% return %INNORETURN%
echo Close or hit to make release
if exist %DISTDIR% rmdir /S/Q %DISTDIR%\
IF EXIST inno_setup.iss del inno_setup.iss

call release.bat
echo release.bat finished, hit to close
::pause
exit
