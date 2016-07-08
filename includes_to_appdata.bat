@echo off
IF NOT DEFINED INCLUDESDIR (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED APPDIR (EXIT)
xcopy /Y /E "%INCLUDESDIR%\ico" "%APPDIR%\ico\"
xcopy /Y /E "%INCLUDESDIR%\dns" "%APPDIR%\dns\"
copy /Y "%INCLUDESDIR%\cacert_ovpn.pem" "%APPDIR%\"

copy /Y "%INCLUDESDIR%\themes\ms-windows.ini" "%PY32%\Lib\site-packages\gnome\etc\gtk-3.0\settings.ini"
xcopy /Y /E "%INCLUDESDIR%\themes\MS-Windows" "%PY32%\Lib\site-packages\gnome\share\themes\MS-Windows\"

::copy /Y "%INCLUDESDIR%\themes\adwaita.ini" "%PY32%\Lib\site-packages\gnome\etc\gtk-3.0\settings.ini"
::xcopy /Y /E "%INCLUDESDIR%\themes\Adwaita" "%PY32%\Lib\site-packages\gnome\share\themes\Adwaita\"

::copy /Y "%INCLUDESDIR%\themes\greybird.ini" "%PY32%\Lib\site-packages\gnome\etc\gtk-3.0\settings.ini"
::xcopy /Y /E "%INCLUDESDIR%\themes\Greybird" "%PY32%\Lib\site-packages\gnome\share\themes\Greybird\"


echo copied includes to appdata '%APPDIR%'
