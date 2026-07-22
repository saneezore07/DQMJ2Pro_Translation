[app]

title = DQMJ2Patcher
package.name = dqmj2patcher
package.domain = org.dqmj2protranslation

source.dir = ../../..
source.include_exts = py,txt,csv,bin,asm,e,json,md,NFTR,png
source.exclude_dirs = .git,.github,GUI_WORK,ANDROID_WORK,__pycache__,build,dist

version = 1.0.1

requirements = python3,kivy,pillow

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 35
android.build_tools_version = 35.0.0
android.minapi = 23
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
