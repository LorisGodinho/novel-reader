# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['novel_reader_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('novels', 'novels'),
        ('src', 'src'),
        ('extratores', 'extratores'),
        ('core', 'core'),
        ('config', 'config'),
    ],
    hiddenimports=[
        'edge_tts',
        'pygame',
        'tkinter',
        'asyncio',
        'json',
        'bs4',
        'bs4.builder._lxml',
        'lxml',
        'lxml.etree',
        'lxml._elementpath',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='NovelReader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Não mostrar console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='NovelReader',
)
