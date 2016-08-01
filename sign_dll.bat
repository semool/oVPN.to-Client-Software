@echo off
IF NOT DEFINED EXESTRING (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED DISTDIR (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED SIGNTOOL (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT EXIST %SIGNTOOL% (echo %SIGNTOOL% NOT FOUND && PAUSE && EXIT)

for %%v in ("%DISTDIR%\*.dll") do (
	for %%A in ("%%v") do (
		IF NOT EXIST %DLLDIR_U%\%%~nxA (
			echo copy /Y "%%v" "%DLLDIR_U%\"
			copy /Y "%%v" "%DLLDIR_U%\"
		)
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
				echo copy /Y "%%v" "%DLLDIR_S%\"
				copy /Y "%%v" "%DLLDIR_S%\"
			)
		) else (
			echo copy /Y "%DLLDIR_S%\%%~nxA" "%DISTDIR%\"
			copy /Y "%DLLDIR_S%\%%~nxA" "%DISTDIR%\"
		)
	)
)

for %%v in ("%DISTDIR%\lib\gtk-3.0\3.0.0\theming-engines\*.dll") do (
	for %%A in ("%%v") do (
		IF NOT EXIST %DLLDIR_U%\%%~nxA (
			echo copy /Y "%%v" "%DLLDIR_U%\"
			copy /Y "%%v" "%DLLDIR_U%\"
		)
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
				echo copy /Y "%%v" "%DLLDIR_S%\"
				copy /Y "%%v" "%DLLDIR_S%\"
			)
		) else (
			echo copy /Y "%DLLDIR_S%\%%~nxA" "%DISTDIR%\lib\gtk-3.0\3.0.0\theming-engines\"
			copy /Y "%DLLDIR_S%\%%~nxA" "%DISTDIR%\lib\gtk-3.0\3.0.0\theming-engines\"
		)
	)
)

for %%v in ("%DISTDIR%\*.pyd") do (
	for %%A in ("%%v") do (
		IF NOT EXIST %DLLDIR_U%\%%~nxA (
			copy /Y "%%v" "%DLLDIR_U%\"
		)
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
				echo copy /Y "%%v" "%DLLDIR_S%\"
				copy /Y "%%v" "%DLLDIR_S%\"
			)
		) else (
			echo copy /Y "%DLLDIR_S%\%%~nxA" "%DISTDIR%\"
			copy /Y "%DLLDIR_S%\%%~nxA" "%DISTDIR%\"
		)
	)
)

echo SIGN_DLL complete
