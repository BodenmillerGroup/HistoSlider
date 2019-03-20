# -*- mode: python -*-

import os

pathex = os.path.abspath(os.path.join(SPECPATH, '..'))

block_cipher = None


a = Analysis(['../histoslider/__main__.py'],
             pathex=[pathex],
             binaries=[],
             datas=[],
             hiddenimports=['pywt._extensions._cwt'],
             hookspath=['setup/hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='histoslider',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='resources\\icons\\app.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='histoslider')

app = BUNDLE(coll,
             name='histoslider.app',
             icon='resources/icons/app.icns',
             bundle_identifier=None)
