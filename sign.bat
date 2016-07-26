@echo off
IF NOT DEFINED EXESTRING (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED DISTDIR (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED SIGNTOOL (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT EXIST %SIGNTOOL% (echo %SIGNTOOL% NOT FOUND && PAUSE && EXIT)

IF EXIST "%DISTDIR%\ovpn_client.exe" (
	%SIGNTOOL% sign /sha1 0775a45c76fad6989cbeb35c87e476642ccc172f /t http://timestamp.verisign.com/scripts/timestamp.dll /fd SHA512 "%DISTDIR%\ovpn_client.exe"
	for %%v in (%DISTDIR%\*.dll) do (
		IF NOT "%%v" == "%DISTDIR%\libgtk-3-0.dll" (
			%SIGNTOOL% sign /sha1 0775a45c76fad6989cbeb35c87e476642ccc172f /t http://timestamp.verisign.com/scripts/timestamp.dll /fd SHA512 "%%v"
		)
	)
)
echo SIGN complete
pause