@echo off
IF NOT DEFINED VERSION (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED BITS (EXIT)
set BINSDIR=%RELEASEDIR%\bins
set DEVSDIR=%RELEASEDIR%\devs
set DEVDIST=%DEVSDIR%\%VERSION%
mkdir %DEVSDIR%
mkdir %DEVDIST%
mkdir %BINSDIR%

xcopy /Y /E "%INCLUDESDIR%" "%DEVDIST%\includes\"
del "%DEVDIST%\includes\crypt32*.dll"

copy /Y "%SOURCEDIR%\%EXESTRING%" "%BINSDIR%\%EXESTRING%"
copy /Y "%SOURCEDIR%\ovpn_client.py" "%DEVDIST%\"
copy /Y "%SOURCEDIR%\setup.py" "%DEVDIST%\"
copy /Y "%SOURCEDIR%\7zSFXcfg%BITS%.txt" "%DEVDIST%\"
copy /Y "%SOURCEDIR%\build.bat" "%DEVDIST%\"
copy /Y "%SOURCEDIR%\debug.bat" %DEVDIST%\"
copy /Y "%SOURCEDIR%\README.md" %DEVDIST%\"
copy /Y "%SOURCEDIR%\release.bat" %DEVDIST%\"

set BUILDDEVFILE=%DEVSDIR%\build-dev-%VERSION%.7z
IF EXIST %BUILDDEVFILE% (del %BUILDDEVFILE%)
%EXE7Z% a -mx9 -t7z "%BUILDDEVFILE%" "%DEVDIST%\"
echo released %EXESTRING%
echo copied binary to: '%BINSDIR%\%EXESTRING%' 
echo copied dev-imports to: '%DEVDIST%'