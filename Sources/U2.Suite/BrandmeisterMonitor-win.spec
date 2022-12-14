# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['BrandmeisterMonitor.py'],
    pathex=['.'],
    binaries=[
        ('icon\\*.png','icon'),
        ('font\\*.ttf','font')
        ],
    datas=[('data\\*','data')],
    hiddenimports=['semver','socketio','dicttoxml'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
    )
pyz = PYZ(
    a.pure, 
    a.zipped_data,
    cipher=block_cipher
    )
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BrandmeisterMonitor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    target_arch=None,
    )
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BrandmeisterMonitor',
)
