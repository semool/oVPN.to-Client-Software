
# oVPN.to Client Software for Windows

## Setup 32/64 Bit Dev-Env
### 

### 32 Bit Downloads
+ [Python 3.4.4 win32](https://www.python.org/ftp/python/3.4.4/python-3.4.4.msi) (install to C:\Python34)

### 64 Bit Downloads
+ [Python 3.4.4 win64](https://www.python.org/ftp/python/3.4.4/python-3.4.4.amd64.msi) (install to C:\Python34_64)

### 32 and 64 Bit
+ !!! When both Envirenments should be installed at the same time it is important that you first install 32 Bit, then 64 Bit and 32 Bit again!!!
+ open cmd.exe as admin:
```
C:\Python34[_64]\Scripts\pip.exe install --upgrade pip
C:\Python34[_64]\Scripts\pip.exe install requests
C:\Python34[_64]\Scripts\pip.exe install requests[security]
C:\Python34[_64]\Scripts\pip.exe install py2exe
C:\Python34[_64]\Scripts\pip.exe install pypiwin32
```
+ Download [hooks.py](else/python/hooks.py) and replace it in ```C:\Python34[_64]\lib\site-packages\py2exe\```

### 32 Bit:
```
C:\Python34\Scripts\pip.exe install netifaces
```


### 64 Bit:
+ Download [netifaces-0.10.5-cp34-cp34m-win_amd64.whl](else/python/netifaces-0.10.5-cp34-cp34m-win_amd64.whl) and place it in ```C:\Python34_64\Scripts```
```
C:\Python34_64\Scripts\pip.exe install netifaces-0.10.5-cp34-cp34m-win_amd64.whl
```

## Basic Requirements
+ [PyGObject 3.18.2rev10 AIO](https://sourceforge.net/projects/pygobjectwin32/files/pygi-aio-3.18.2_rev10-setup_84c21bc2679ff32e73de38cbaa6ef6d30c628ae5.exe/download) Select only: 'Base packages' + 'GTK+ 3.18.9' and install into 32 and 64 bit!
+ [Visual C++ 2010 Express] (http://www.chip.de/downloads/Visual-C-2010-Express_24081894.html)
+ [Inno Setup 5.5.9](http://www.jrsoftware.org/download.php/is.exe)
+ [poedit 1.8.10](https://download.poedit.net/Poedit-1.8.10-setup.exe)

## Developer Imports: how to run or build from source
### Debug Mode
+ create a link (name: DEBUG32) to debug.bat: edit link, set target:
+ ```X:\????\ovpn-client\debug.bat 32``` and run link as admin!
+ for Debug Mode with more debug messages set target:
+ ```X:\????\ovpn-client\debug.bat 32 DEVMODE```
+ same for 64 bits and do NOT run any of the *.bat files directly!

### Build Mode
+ create a link (name: BUILD32) to build_inno.bat: edit link, set target:
+ ```'X:\????\ovpn-client\build_inno.bat 32``` and run link normally!
+ to run in Sign Mode set target:
+ ```X:\????\ovpn-client\build_inno.bat 32 SIGN```
+ edit ```set_dirs.bat``` to your needs!
+ Update VERSION only in file: ```release_version.py```
+ Set SIGN in ```release_version.py``` to False for unsigned inno compile
+ same for 64 bits and do NOT run any of the *.bat files directly!

## Self Signed Certificate
+ Download and install SDK for your OS 
+ [Microsoft Windows SDK for Windows 7](https://download.microsoft.com/download/A/6/A/A6AC035D-DA3F-4F0C-ADA4-37C8E5D34E3D/winsdk_web.exe) Select only: '.Net Development' -> 'Tools'
+ [Microsoft Windows SDK for Windows 8](https://go.microsoft.com/fwlink/p/?LinkId=226658)
+ [Microsoft Windows SDK for Windows 10](https://go.microsoft.com/fwlink/p/?LinkID=698771) Select only: 'Windows App Certification Kit'
+ [DigiCert Certificate Utility for Windows](https://www.digicert.com/util/DigiCertUtil.zip)
+ open cmd.exe as admin:
+ ```makecert.exe -n "CN=oVPN.to-Client, O=organizationName, OU=organizationalUnitName, L=localityName, S=stateOrProvinceName, C=countryName" -a sha512 -r -cy authority -pe -ss root -sr currentuser -len 4096 -h 3```
+ ```makecert.exe -n "CN=oVPN.to-Client, L=localityName, S=stateOrProvinceName, C=countryName" -a sha512 -pe -ss my -sr currentuser -in "oVPN.to-Client" -is root -ir currentuser -len 4096 -eku 1.3.6.1.5.5.7.3.3```
+ Open DigiCertUtil.exe and it shows your Certificate
+ Right click your Certificate and select "copy thumbprint to clipboard"
+ Edit ```set_dirs.bat``` and replace the ```SIGNCERTSHA1``` with the one in clipboard

## Inno Setup Sign Tools
+ Open InnoSetup and goto: ```Tools``` -> ```Configure Sign Tools...``` -> ```Add```
+ name: signtool1 [OK] command:
+ ```"Path to signtool.exe (e.g. 'C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe')" sign /v /sha1 YourThumbprint /fd sha1 /t http://timestamp.comodoca.com/?td=sha1 $f```
+ + name: signtool2 [OK] command:
+ ```"Path to signtool.exe (e.g. 'C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe')" sign /v /as /sha1 YourThumbprint /fd sha256 /td sha256 /tr http://timestamp.comodoca.com/?td=sha256 $f```
+ name: signtool3 [OK] command:
+ ```"Path to signtool.exe (e.g. 'C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe')" sign /v /as /sha1 YourThumbprint /fd sha384 /td sha384 /tr http://timestamp.comodoca.com/?td=sha384 $f```
+ name: signtool4 [OK] command:
+ ```"Path to signtool.exe (e.g. 'C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe')" sign /v /as /sha1 YourThumbprint /fd sha512 /td sha512 /tr http://timestamp.comodoca.com/?td=sha512 $f```

## Generate locales
+ create a link (name: GENERATE_PO32) to generate_po.bat: edit link, set target:
+ ```'X:\????\ovpn-client\generate_po.bat 32``` and run link normally!
+ start [poedit 1.8.10](https://download.poedit.net/Poedit-1.8.10-setup.exe)
+ open file ```X:\????\ovpn-client\locale\[lang]\ovpn_client.po```
+ catalog -> update from POT -> './messages.pot'
