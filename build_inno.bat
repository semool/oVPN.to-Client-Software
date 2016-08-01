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
IF EXIST inno_setup.iss del inno_setup.iss

echo hit to compile py2exe: %BINARY%
pause
echo compiling...
%PYEXE% -OO setup.py py2exe 1> %PY2EXE_LOG% 2> %PY2EXE_ERR%
echo py2exe compiled with exitcode %errorlevel%: logfile: %PY2EXE_LOG%

for %%F in (%SOURCEDIR%\py2exe*.log) do if %%~zF equ 0 del %%F
IF EXIST %PY2EXE_ERR% (
	echo errors in py2exe
	notepad.exe %PY2EXE_ERR%
	exit
)

echo py2exe completed
echo Close or hit to continue with includes_to_dist
pause

call includes_to_dist.bat %~1
if exist %WORKPATH% rmdir /S/Q %WORKPATH%\
if exist %SOURCEDIR%\tmp\ rmdir /S/Q %SOURCEDIR%\tmp\
IF EXIST %PY2EXE_LOG% del %PY2EXE_LOG%
del "%SOURCEDIR%\*.pyc" 2> nul
del "%SOURCEDIR%\*.pyo" 2> nul
echo includes_to_dist.bat completed
IF "%~2" == "SIGN" (
	echo Close or hit to continue with Sign
) else (
	echo Close or hit to continue with compile: inno_setup.iss
)
pause

IF "%~2" == "SIGN" (
	call sign_exe.bat
	call sign_dll.bat
	)

IF "%~2" == "SIGN" (
	echo Close or hit to compile: inno_setup.iss
	pause
)
%INNOCOMPILE% /cc "%SOURCEDIR%\inno_setup.iss"

echo Inno Setup %EXESTRING%
echo Close or hit to make release
pause

call release.bat
echo release.bat finished, close or hit to cleanup
pause

if exist %DISTDIR% rmdir /S/Q %DISTDIR%\
IF EXIST inno_setup.iss del inno_setup.iss
