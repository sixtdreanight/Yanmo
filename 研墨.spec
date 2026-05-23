# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('C:\\Users\\DreamNight\\Documents\\01My\\ai\\科研助手\\backend', 'backend')]
binaries = []
hiddenimports = ['backend.core.event_bus', 'backend.core.config', 'backend.core.security', 'backend.core.storage', 'backend.core.llm_router', 'backend.core.engine', 'backend.core.scheduler', 'backend.plugins', 'chromadb', 'sympy', 'feedparser', 'aiohttp', 'sentence_transformers', 'PySide6']
tmp_ret = collect_all('chromadb')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('sentence_transformers')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['C:\\Users\\DreamNight\\Documents\\01My\\ai\\科研助手\\frontend_qt\\main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='研墨',
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
    icon=['C:\\Users\\DreamNight\\Documents\\01My\\ai\\科研助手\\frontend\\src-tauri\\icons\\icon.ico'],
)
