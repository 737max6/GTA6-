# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['GTA6抢先版安装程序v2.0.py'],
    pathex=[],
    binaries=[],
    datas=[('Jason_and_Lucia_Robbery_With_Logo_square.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GTA6_Installer_v2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['Jason_and_Lucia_Robbery_With_Logo_square.ico'],
)
