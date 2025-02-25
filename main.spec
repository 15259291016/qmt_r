# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
from PyInstaller.building.datastruct import Tree

block_cipher = None

a = Analysis(
    ['main.py'],  # 你的主脚本文件
    pathex=[],  # 可以添加额外的路径
    binaries=[],
    datas=[
        ('Config', 'Config'),       # 包含 Config 目录
        ('DbServer', 'DbServer'),   # 包含 DbServer 目录
        ('FileCache', 'FileCache'), # 包含 FileCache 目录
        ('logs', 'logs'),           # 包含 logs 目录
        ('ApiServer', 'ApiServer'), # 包含 ApiServer 目录
        ('BotServer', 'BotServer'), # 包含 BotServer 目录
        ('OutPut', 'OutPut'),       # 包含 OutPut 目录
        ('PushServer', 'PushServer'), # 包含 PushServer 目录
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',  # 输出可执行文件的名称
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
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
    name='main',  # 显式设置 COLLECT 的 name 参数
    strip=False,
    upx=True,
)