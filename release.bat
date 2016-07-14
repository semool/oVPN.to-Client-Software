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
del "%DEVDIST%\includes\crypt32*.dll"

copy /Y "%SOURCEDIR%\%EXESTRING%" "%BINSDIR%\%EXESTRING%"
del "%SOURCEDIR%\%EXESTRING%"
copy /Y "%SOURCEDIR%\ovpn_client.py" "%DEVDIST%\"
copy /Y "%SOURCEDIR%\setup.py" "%DEVDIST%\"
copy /Y "%SOURCEDIR%\7zSFXcfg%BITS%.txt" "%DEVDIST%\"
copy /Y "%SOURCEDIR%\*.bat" "%DEVDIST%\"
copy /Y "%SOURCEDIR%\inno_setup%BITS%.iss" "%DEVDIST%\"

set BUILDDEVFILE=%DEVSDIR%\build-dev-%VERSION%.7z
IF EXIST %BUILDDEVFILE% (del %BUILDDEVFILE%)
%EXE7Z% a -mx9 -t7z "%BUILDDEVFILE%" "%DEVDIST%\"
echo released %EXESTRING%
echo copied binary to: '%BINSDIR%\%EXESTRING%' 
echo copied dev-imports to: '%DEVDIST%'
