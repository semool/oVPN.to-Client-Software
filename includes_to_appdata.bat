@echo off
IF NOT DEFINED INCLUDESDIR (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED APPDIR (EXIT)
xcopy /Y /E "%INCLUDESDIR%\ico" "%APPDIR%\ico\"
xcopy /Y /E "%INCLUDESDIR%\dns" "%APPDIR%\dns\"
copy /Y "%INCLUDESDIR%\cacert_ovpn.pem" "%APPDIR%\"
echo copied includes to appdata '%APPDIR%'
