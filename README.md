
# oVPN.to Client Software for Windows

## Setup 32 Bit Dev-Env:
+ [Python 2.7.12 win32](https://www.python.org/ftp/python/2.7.12/python-2.7.12.msi) (install to C:\Python27) !!!
+ [py2exe 0.6.9 win32](http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/py2exe-0.6.9.win32-py2.7.exe/download)

+ open cmd.exe as admin:
+ C:\Python27\Scripts\pip.exe install --upgrade pip
+ C:\Python27\Scripts\pip.exe install pycrypto (not needed atm)
+ C:\Python27\Scripts\pip.exe install --upgrade pycrypto 
+ C:\Python27\Scripts\pip.exe install requests
+ C:\Python27\Scripts\pip.exe install --upgrade requests
+ C:\Python27\Scripts\pip.exe install netifaces
+ C:\Python27\Scripts\pip.exe install --upgrade netifaces


## Setup 64 Bit Dev-Env:
+ [Python 2.7.12 win64](https://www.python.org/ftp/python/2.7.12/python-2.7.12.amd64.msi) (install to C:\Python27_64) !!!
+ [py2exe 0.6.9 win64](http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/py2exe-0.6.9.win64-py2.7.amd64.exe/download)

+ open cmd.exe as admin:
+ C:\Python27_64\Scripts\pip.exe install --upgrade pip
+ C:\Python27_64\Scripts\pip.exe install pycrypto (not needed atm)
+ C:\Python27_64\Scripts\pip.exe install --upgrade pycrypto 
+ C:\Python27_64\Scripts\pip.exe install requests
+ C:\Python27_64\Scripts\pip.exe install --upgrade requests
+ C:\Python27_64\Scripts\pip.exe install netifaces
+ C:\Python27_64\Scripts\pip.exe install --upgrade netifaces

## Basic Requirements:
+ [PyGObject 3.18.2 AIO](https://sourceforge.net/projects/pygobjectwin32/files/pygi-aio-3.18.2_rev7-setup.exe/download) Select only: 'Base packages' + 'GTK+ 3.18.9' and install into 32 and 64 bit!
+ [Microsoft Visual C++ Compiler for Python 2.7](http://www.microsoft.com/en-us/download/details.aspx?id=44266)
+ [Inno Setup 5.5.9](http://www.jrsoftware.org/download.php/is.exe)

## Developer Imports: how to run or build from source
+ create a link (name: DEBUG32) to debug.bat: edit link, set target 'X:\????\ovpn-client\debug.bat 32' and run link as admin!
+ create a link (name: BUILD32) to build_inno.bat: edit link, set target 'X:\????\ovpn-client\build_inno.bat 32' and run link normally!
+ same for 64 bits and do NOT run any of the *.bat files directly!
+ edit 'set_dirs.bat' to your needs!
+ Update Version only in file: 'release_version.py'

## Generate locales:
+ run generate_po.bat
+ start poedit 1.8+
+ open file 'locale/de/ovpn_client.po'
+ catalog -> update from POT -> './messages.pot'

## Self Signed Certificate
+ Download and install SDK for your OS 
+ [Microsoft Windows SDK for Windows 7](https://download.microsoft.com/download/A/6/A/A6AC035D-DA3F-4F0C-ADA4-37C8E5D34E3D/winsdk_web.exe) Select only: '.Net Development' -> 'Tools'
+ [Microsoft Windows SDK for Windows 8](https://go.microsoft.com/fwlink/p/?LinkId=226658)
+ [Microsoft Windows SDK for Windows 10](https://go.microsoft.com/fwlink/p/?LinkID=698771) Select only: 'Windows App Certification Kit'
+ [DigiCert Certificate Utility for Windows](https://www.digicert.com/util/DigiCertUtil.zip)
+ open cmd.exe as admin:
+ makecert.exe -n "CN=oVPN.to-Client, O=organizationName, OU=organizationalUnitName, L=localityName, S=stateOrProvinceName, C=countryName" -a sha512 -r -cy authority -pe -ss root -sr currentuser -len 4096 -h 3
+ makecert.exe -n "CN=oVPN.to-Client, L=localityName, S=stateOrProvinceName, C=countryName" -a sha512 -pe -ss my -sr currentuser -in "oVPN.to-Client" -is root -ir currentuser -len 4096 -eku 1.3.6.1.5.5.7.3.3
+ Open DigiCertUtil.exe and it shows your Certificate
+ Right click your Certificate and select "copy thumbprint to clipboard"
+ Edit sign.bat and replace the thumbprints with the one in clipboard

## Inno Setup Sign Tools: "Tools" -> "Configure Sign Tools..." -> Add
+ name: signtool1 [OK] command: "Path to signtool.exe (e.g. 'C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe')" sign /v /sha1 YourThumbprint /fd sha1 /t http://timestamp.comodoca.com/?td=sha1 $f
+ name: signtool2 [OK] command: "Path to signtool.exe (e.g. 'C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe')" sign /v /as /sha1 YourThumbprint /fd sha256 /td sha256 /tr http://timestamp.comodoca.com/?td=sha256 $f
+ name: signtool3 [OK] command: "Path to signtool.exe (e.g. 'C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe')" sign /v /as /sha1 YourThumbprint /fd sha384 /td sha384 /tr http://timestamp.comodoca.com/?td=sha384 $f
+ name: signtool4 [OK] command: "Path to signtool.exe (e.g. 'C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe')" sign /v /as /sha1 YourThumbprint /fd sha512 /td sha512 /tr http://timestamp.comodoca.com/?td=sha512 $f
