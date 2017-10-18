#!user/bin/env python
# -*- coding: utf-8 -*-

import os

import CommonUtils

if __name__ == '__main__':
    fileList = CommonUtils.getAllFileFromCurrentDir("apk")
    for apk in fileList:
        command = "adb install -r " + apk
        print command
        os .system(command)






