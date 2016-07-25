@echo off
IF NOT DEFINED VERSION (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED BITS (EXIT)
set BINSDIR=%RELEASEDIR%\bins\%RELEASE%
set DEVSDIR=%RELEASEDIR%\devs\%RELEASE%
set DEVDIST=%DEVSDIR%\%VERSION%
mkdir %DEVSDIR%
mkdir %DEVDIST%
mkdir %BINSDIR%

xcopy /Y /E "%INCLUDESDIR%" "%DEVDIST%\includes\"
xcopy /Y /E "%LOCALEDIR%" "%DEVDIST%\locale\"
IF "%BITS%" == "32" ( rd /S /Q "%DEVDIST%\includes\Microsoft.VC90.CRT_win64" 2>nul )
IF "%BITS%" == "64" ( rd /S /Q "%DEVDIST%\includes\Microsoft.VC90.CRT_win32" 2>nul )

copy /Y "%SOURCEDIR%\%EXESTRING%" "%BINSDIR%\%EXESTRING%"
del "%SOURCEDIR%\%EXESTRING%"
copy /Y "%SOURCEDIR%\ovpn_client.py" "%DEVDIST%\"
copy /Y "%SOURCEDIR%\setup.py" "%DEVDIST%\"
copy /Y "%SOURCEDIR%\*.bat" "%DEVDIST%\"
copy /Y "%SOURCEDIR%\inno_setup%BITS%.iss" "%DEVDIST%\"
copy /Y "%SOURCEDIR%\release_version.py" "%DEVDIST%\"
copy /Y "%SOURCEDIR%\set_version.txt" "%DEVDIST%\"

set BUILDDEVFILE=%DEVSDIR%\build-dev-%VERSION%.7z
IF EXIST %BUILDDEVFILE% (del %BUILDDEVFILE%)
%EXE7Z% a -mx9 -t7z "%BUILDDEVFILE%" "%DEVDIST%\"
echo released %EXESTRING%
echo copied binary to: '%BINSDIR%\%EXESTRING%' 
echo copied dev-imports to: '%DEVDIST%'
