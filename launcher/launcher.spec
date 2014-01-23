# -*- mode: python -*-
a = Analysis(['launcher.py'],
             pathex=['C:\\Users\\user\\workspace\\\launcher'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          a.dependencies,
          exclude_binaries=False,
          name='launcher.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )