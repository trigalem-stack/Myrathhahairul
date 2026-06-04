[app]
title = SystemHelper
package.name = securityhelper
package.domain = com.system
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,android,telegram==20.0,requests,firebase-admin,cryptography,pillow
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 1
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,FOREGROUND_SERVICE,SYSTEM_ALERT_WINDOW
android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 30
android.gradle_dependencies = 'com.google.firebase:firebase-database:20.0.0'
android.enable_androidx = true
android.add_src = 
android.add_assets = 
android.sdk_path = /home/runner/work/Myrathhahairul/Myrathhahairul/android-sdk
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25c
