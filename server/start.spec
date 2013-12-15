# -*- mode: python -*-
a = Analysis(['start.py'],
             pathex=['C:\\Users\\user\\workspace\\pstop'],
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
          name='start.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )