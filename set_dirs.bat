@echo off
echo set_dirs.bat
echo %SOURCEDIR%

set PYRAMDISK=%SOURCEDIR%\pyram.y

IF NOT EXIST %PYRAMDISK% (
	set PY32=C:\Python34
	set PY64=C:\Python34_64
	set RAM=0
) ELSE IF EXIST %PYRAMDISK% (
	set PY32=P:\Python34
	set PY64=P:\Python34_64
	set RAM=1
)

set APPDIR=%APPDATA%\ovpn\bin\client\dist
set INNOCOMPILE="C:\Program Files (x86)\Inno Setup 5\Compil32.exe"
set EXE7Z="%PROGRAMFILES%\7-Zip\7z.exe"

set BITS=%~1
set PYCACHE=%SOURCEDIR%\__pycache__
set INCLUDESDIR=%SOURCEDIR%\includes
set LOCALEDIR=%SOURCEDIR%\locale
set DISTDIR=%SOURCEDIR%\dist%BITS%
set DISTDIR2=%SOURCEDIR%\dist_check_bin%BITS%
set DISTDIR3=%SOURCEDIR%\dist_cmd%BITS%
set WORKPATH=%SOURCEDIR%\build%BITS%
set LANGPATH=%DISTDIR%\share\locale\
set BINARY=%DISTDIR%\ovpn_client.exe

set CERTUTIL="C:\Windows\System32\CertUtil.exe"

IF "%BITS%" == "32" ( set SIGNTOOL=%INCLUDESDIR%\codesign\signtool_w10sdk_x86.exe )
IF "%BITS%" == "64" ( set SIGNTOOL=%INCLUDESDIR%\codesign\signtool_w10sdk_x64.exe )
set SIGNCERTSHA1=3096b6b152948d9c8f7f3b76a45221c1177ee8d3


IF NOT EXIST %CERTUTIL% (echo %CERTUTIL% NOT FOUND && PAUSE && EXIT)
IF NOT EXIST %SIGNTOOL% (echo %SIGNTOOL% NOT FOUND && PAUSE && EXIT)

REM DONT CHANGE DOWN HERE !

set SIGNTOOLCMD1=%SIGNTOOL% sign /v /sha1 %SIGNCERTSHA1% /fd sha1 /t http://timestamp.comodoca.com/?td=sha1
::set SIGNTOOLCMD2=%SIGNTOOL% sign /v /as /sha1 %SIGNCERTSHA1% /fd sha256 /td sha256 /tr http://timestamp.comodoca.com/?td=sha256
::set SIGNTOOLCMD3=%SIGNTOOL% sign /v /as /sha1 %SIGNCERTSHA1% /fd sha384 /td sha384 /tr http://timestamp.comodoca.com/?td=sha384
set SIGNTOOLCMD4=%SIGNTOOL% sign /v /as /sha1 %SIGNCERTSHA1% /fd sha512 /td sha512 /tr http://timestamp.comodoca.com/?td=sha512
set SIGNTOOLVERI=%SIGNTOOL% verify /v /a /all /pa /tw /sha1 %SIGNCERTSHA1% 


set PY32EXE=%PY32%\python.exe
set PY64EXE=%PY64%\python.exe
set PY32GET=%PY32%\Tools\i18n
set PY64GET=%PY64%\Tools\i18n

set DLL32_S=%SOURCEDIR%\includes\DLL\32\signed
set DLL32_U=%SOURCEDIR%\includes\DLL\32\unsigned

set DLL64_S=%SOURCEDIR%\includes\DLL\64\signed
set DLL64_U=%SOURCEDIR%\includes\DLL\64\unsigned

IF "%BITS%" == "32" (
	set PYEXE=%PY32EXE%
	set PYGET=%PY32GET%
	set DLLDIR_S=%DLL32_S%
	set DLLDIR_U=%DLL32_U%
	set PYINSTALLER=%PY32%\Scripts\pyinstaller.exe
)

IF "%BITS%" == "64" (
	set PYEXE=%PY64EXE%
	set PYGET=%PY64GET%
	set DLLDIR_S=%DLL64_S%
	set DLLDIR_U=%DLL64_U%
	set PYINSTALLER=%PY64%\Scripts\pyinstaller.exe
)

IF NOT DEFINED PYEXE (echo MISSING BITS && PAUSE && EXIT)
IF NOT EXIST %PYEXE% (echo PYEXE %PYEXE% NOT FOUND && PAUSE && EXIT)
::IF NOT EXIST %PYINSTALLER% (echo PYINSTALLER %PYINSTALLER% NOT FOUND && PAUSE && EXIT)


set PY2EXE_LOG=%SOURCEDIR%\py2exe_%BITS%.log
set PY2EXE_ERR=%SOURCEDIR%\py2exe_ERR_%BITS%.log

echo dir vars loaded
echo %SOURCEDIR%
