# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['D:\\Workspace\\UET_CAM\\src\\Release V2'],
             binaries=[],
             datas=[('D:\\Workspace\\UET_CAM\\src\\Release V2\\new_cropped', 'new_cropped'), ('D:\\Workspace\\UET_CAM\\src\\Release V2\\logo\\uet.png', 'logo'), ('D:\\Workspace\\UET_CAM\\src\\Release V2\\logo\\close.jpg', 'logo'), ('D:\\Workspace\\UET_CAM\\src\\Release V2\\center.txt', '.')],
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
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='logo\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
