@echo off
IF NOT DEFINED VERSION (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED BITS (EXIT)
set BINSDIR=%RELEASEDIR%\bins\%RELEASE%
set DEVSDIR=%RELEASEDIR%\devs\%RELEASE%
set DEVDIST=%DEVSDIR%\%VERSION%
mkdir %DEVSDIR%
mkdir %DEVDIST%
mkdir %BINSDIR%

mkdir "%DEVDIST%\includes\"
mkdir "%DEVDIST%\includes\codesign"
mkdir "%DEVDIST%\else\"
mkdir "%DEVDIST%\else\app_icons"
xcopy /Y /E "%INCLUDESDIR%\themes" "%DEVDIST%\includes\themes\"
xcopy /Y /E "%INCLUDESDIR%\Microsoft.VC90.CRT_win%BITS%" "%DEVDIST%\includes\Microsoft.VC90.CRT_win%BITS%\"
xcopy /Y /E "%LOCALEDIR%" "%DEVDIST%\locale\"
copy /Y "%SIGNTOOL%" "%DEVDIST%\includes\codesign\"
copy /Y "%INCLUDESDIR%\cacert_ovpn.pem" "%DEVDIST%\includes\"
copy /Y "%SOURCEDIR%\else\app_icons\shield_exe*" "%DEVDIST%\else\app_icons"
copy /Y "%SOURCEDIR%\%EXESTRING%" "%BINSDIR%\%EXESTRING%"
copy /Y "%SOURCEDIR%\ovpn_client.py" "%DEVDIST%\"
copy /Y "%SOURCEDIR%\*.py" "%DEVDIST%\"
copy /Y "%SOURCEDIR%\*.bat" "%DEVDIST%\"
del "%SOURCEDIR%\%EXESTRING%"
rmdir /S/Q %PYCACHE%\

set BUILDDEVFILE=%DEVSDIR%\build-dev-%VERSION%.7z
IF EXIST %BUILDDEVFILE% (del %BUILDDEVFILE%)
%EXE7Z% a -mx9 -t7z "%BUILDDEVFILE%" "%DEVDIST%\"
echo released %EXESTRING%
echo copied binary to: '%BINSDIR%\%EXESTRING%' 
echo copied dev-imports to: '%DEVDIST%'
