# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Projects\\Valdek_caris_line_converter'],
             binaries=[],
             datas=[('img/icon.png', 'img')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Waldi\'s Caris lines converter',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , version='version_info.txt', icon='icon.ico')