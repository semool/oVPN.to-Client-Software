@echo off
IF NOT DEFINED EXESTRING (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED DISTDIR (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED SIGNTOOL (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT EXIST %SIGNTOOL% (echo %SIGNTOOL% NOT FOUND && PAUSE && EXIT)

for %%v in ("%DISTDIR%\*.dll") do (
	for %%A in ("%%v") do (
		IF NOT EXIST %DLLDIR_S%\%%~nxA (
			IF DEFINED SIGNTOOLCMD1 (%SIGNTOOLCMD1% "%%v")
			IF DEFINED SIGNTOOLCMD4 (%SIGNTOOLCMD4% "%%v")
			IF DEFINED SIGNTOOLVERI (
				echo VERIFY: %%v
				%SIGNTOOLVERI% "%%v"
			)
			IF NOT EXIST %DLLDIR_S% (
				echo !!ATTENTION!! Create %DLLDIR_S% to save signed DLL
			) else (
				copy /Y "%%v" "%DLLDIR_S%\"
			)
		) else (
			copy /Y "%DLLDIR_S%\%%~nxA" "%DISTDIR%\"
		)
	)
)
echo SIGN_DLL complete
pause