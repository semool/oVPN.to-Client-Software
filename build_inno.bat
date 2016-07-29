@echo off
set SOURCEDIR=%~dp0.

call %SOURCEDIR%\set_dirs.bat %~1

IF NOT DEFINED PYEXE (EXIT)

del "%SOURCEDIR%\*.pyc"
del "%SOURCEDIR%\*.pyo"

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
IF EXIST py2exe_error.log del py2exe_error.log
IF EXIST py2exe.log del py2exe.log

echo py2exe compile: %BINARY%
%PYEXE% -OO setup.py py2exe 1> py2exe.log 2> py2exe_error.log
echo py2exe compiled with exitcode %errorlevel%: logfile: py2exe.log

for %%F in (%SOURCEDIR%\py2exe*.log) do if %%~zF equ 0 del %%F
IF EXIST py2exe_error.log (
	echo errors in py2exe
	notepad.exe py2exe_error.log
	exit
)

call includes_to_dist.bat %~1
echo includes_to_dist.bat completed
pause


IF "%~2" == "SIGN" (
	echo hit to SIGN files in %DISTDIR%
	for %%v in (%DISTDIR%\*.exe) do (
		echo sign?: %%v
	)
	pause
	call sign_exe.bat
	)


echo hit to compile: inno_setup%BITS%.iss
pause
%INNOCOMPILE% /cc "%SOURCEDIR%\inno_setup%BITS%.iss"

echo Inno Setup %EXESTRING%
echo Close or hit to make release
pause

call release.bat
echo release.bat finished, close or hit to cleanup
pause

if exist %DISTDIR% rmdir /S/Q %DISTDIR%\
if exist %WORKPATH% rmdir /S/Q %WORKPATH%\
if exist %SOURCEDIR%\tmp\ rmdir /S/Q %SOURCEDIR%\tmp\