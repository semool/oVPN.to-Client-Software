@echo off
IF NOT DEFINED EXESTRING (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
if exist "%DISTDIR%\ovpn_client.exe" (signtool sign /v /a /sha1 "0775a45c76fad6989cbeb35c87e476642ccc172f" /t http://timestamp.verisign.com/scripts/timestamp.dll /fd SHA512 "%DISTDIR%\ovpn_client.exe" && pause)
if exist %EXESTRING% (signtool sign /v /a /sha1 "0775a45c76fad6989cbeb35c87e476642ccc172f" /t http://timestamp.verisign.com/scripts/timestamp.dll /fd SHA512 %EXESTRING% && pause)
pause

