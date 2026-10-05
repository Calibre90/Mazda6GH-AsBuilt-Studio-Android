[app]
title = Mazda 6 GH As-Built Studio
package.name = mazda6ghasbuilt
package.domain = org.d3dimone
source.dir = .
source.include_exts = py,png,jpg,jpeg,json,abt,txt,kv
version = 2.4
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png
android.api = 35
android.minapi = 26
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
