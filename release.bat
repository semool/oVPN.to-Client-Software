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
copy /Y %EXESTRING %BINSDIR%\
copy /Y ovpn_client.py %DEVDIST%\
copy /Y setup.py %DEVDIST%\
copy /Y 7zSFXcfg%BITS%.txt %DEVDIST%\
copy /Y build%BITS%.bat %DEVDIST%\
copy /Y debug%BITS%.bat %DEVDIST%\
copy /Y README.md %DEVDIST%\
copy /Y release.bat %DEVDIST%\


%EXE7Z% a -mx9 -t7z "%DEVSDIR%\build-dev-%VERSION%.7z" %DEVDIST%\
echo released %EXESTRING%
echo copied binary to: '%BINSDIR%\%EXESTRING%' 
echo copied dev-imports to: '%DEVDIST%'