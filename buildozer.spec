[app]
title = PDF Extractor
package.name = pdfextractor
package.domain = org.test

source.dir = .
source.include_exts = py

version = 0.1

requirements = python3==3.10.11,kivy==2.2.0,pymupdf==1.23.7,pandas==1.5.3,plyer

orientation = portrait

android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.accept_sdk_license = True
