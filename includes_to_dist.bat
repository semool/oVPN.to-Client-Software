@echo off
IF NOT DEFINED INCLUDESDIR (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED DISTDIR (EXIT)

copy /Y "%INCLUDESDIR%\cacert_ovpn.pem" "%DISTDIR%\"
xcopy /Y /E "%INCLUDESDIR%\ico" "%DISTDIR%\ico\"
xcopy /Y /E "%INCLUDESDIR%\dns" "%DISTDIR%\dns\"
xcopy /Y /E "%LOCALEDIR%" "%DISTDIR%\locale\"

::copy /Y "%INCLUDESDIR%\themes\ms-windows.ini" "%DISTDIR%\etc\gtk-3.0\settings.ini"
::xcopy /Y /E "%INCLUDESDIR%\themes\MS-Windows" "%DISTDIR%\share\themes\MS-Windows\"

::copy /Y "%INCLUDESDIR%\themes\adwaita.ini" "%DISTDIR%\etc\gtk-3.0\settings.ini"
::xcopy /Y /E "%INCLUDESDIR%\themes\Adwaita" "%DISTDIR%\share\themes\Adwaita\"

::copy /Y "%INCLUDESDIR%\themes\greybird.ini" "%DISTDIR%\etc\gtk-3.0\settings.ini"
::xcopy /Y /E "%INCLUDESDIR%\themes\Greybird" "%DISTDIR%\share\themes\Greybird\"

::Install all Themes and use inApp Theme Changer. Default is ms-windows
xcopy /Y /E "%INCLUDESDIR%\themes" "%DISTDIR%\share\themes\"
copy /Y "%INCLUDESDIR%\themes\switcher.ini" "%DISTDIR%\etc\gtk-3.0\settings.ini"

copy /Y "%INCLUDESDIR%\crypt32_win%BITS%.dll" "%DISTDIR%\crypt32.dll"

mkdir "%DISTDIR%\appdata"
echo %RELEASE% > "%DISTDIR%\appdata\version