# -*- mode: python -*-

block_cipher = None


a = Analysis(['E:\\Persoenlich\\ovpn-client\\.\\check_bin.py'],
             pathex=['E:\\Persoenlich\\ovpn-client'],
             #binaries=["C:\\WINDOWS\\system32\\python27.dll"],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=True,
             win_private_assemblies=True,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='check_bin',
          debug=False,
          strip=False,
          upx=False,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='check_bin')
