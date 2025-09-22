[app]

# (str) Title of your application
title = Cảnh Giác Online

# (str) Package name
package.name = canhgiaconline

# (str) Package domain (must be unique)
package.domain = org.lytutrong

# (str) Source code where main.py is located
source.dir = .

# (str) The main .py file
source.main = main.py
    
# (str) Supported orientations
orientation = portrait

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Icon of the application (512x512 PNG)
icon.filename = icon.png

# (str) Presplash of the application
presplash.filename = presplash.png

# (str) Application requirements
# Kivy + KivyMD
requirements = python3,kivy==2.3.0,kivymd==1.2.0

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions (có thể mở rộng sau này)
android.permissions = INTERNET

# (int) Target Android API (>= 31 để upload Play Store)
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android NDK version
android.ndk = 25b

# (int) Android SDK version to use
android.sdk = 33

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1


[buildozer]

# (str) Directory to put the .apk results
bin_dir = bin

# (str) Log level (1 = error, 2 = warn, 3 = info, 4 = debug)
log_level = 2

# (bool) Use zipalign to optimize the APK
zipalign = True
