
:: backup ram to ram
robocopy Q:\ovpn-client\ R:\ovpn-client\ /MIR
pause

:: backup ram to disk
robocopy R:\ovpn-client\ E:\Persoenlich\ovpn-client\ /MIR
echo %ERRORLEVEL%
pause