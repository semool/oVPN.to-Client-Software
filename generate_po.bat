@echo off
set SOURCEDIR=%~dp0.
call %SOURCEDIR%\set_dirs.bat %~1

%PYEXE% %PYGET%\pygettext.py -p %SOURCEDIR%\ -a %SOURCEDIR%\ovpn_client.py

echo "Now install https://poedit.net/ and translate to your language and save mo file under ./locale/language/ (language=de)"
pause