#!user/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
from os.path import join, dirname, realpath

import re

import time


# 获取包名
import shutil

# bsdiff.exe目录
bsdiff_PATH = join(dirname(realpath(__file__)), 'bsdiff')
# patch所在目录
patch_dst_path = os.path.split(os.path.realpath(__file__))[0]+'\\patch\\'

def get_packagename(apk):
    command_getpackagename = "aapt d badging " + apk
    p = subprocess.Popen(command_getpackagename, stdout=subprocess.PIPE, stderr=None, shell=True)
    p_communicate = p.communicate()
    pattern = re.compile(r'package: name=\'(\S+)\'')
    search = pattern.search(p_communicate[0])
    package_name = search.group(1)
    return package_name


# 获取patch
def get_patch(old_apk, new_apk, packagename):
    packagename_split = packagename.split('.')
    packagename_end = packagename_split[-1]
    now_time = str(int(time.time()))
    patch_name = packagename_end + now_time + '.patch'
    command_patch = bsdiff_PATH + ' ' + old_apk + ' ' + new_apk + ' ' + patch_name
    print command_patch
    patch_log = os.popen(
        command_patch).read()
    print patch_log
    # 移动patch
    if not os.path.exists(patch_dst_path):
        os.mkdir(patch_dst_path)

    shutil.move(patch_name,patch_dst_path+patch_name)
    os.system('echo haha!go!go!go!')


if __name__ == '__main__':

    apk_old = raw_input('old_path: ')
    apk_new = raw_input('new_path: ')
    apk_old_list = apk_old.strip().split(' ')
    apk_new_list = apk_new.strip().split(' ')
    print apk_old_list
    print apk_new_list
    for old_index, old_apk in enumerate(apk_old_list):
        # print index,apk
        packagename = get_packagename(old_apk)
        # print index
        for new_index, new_apk in enumerate(apk_new_list):
            second_package_name = get_packagename(new_apk)
            if second_package_name == packagename:
                # print second_index
                print 'same packagename: %s go patch' % second_package_name
                get_patch(old_apk, new_apk, packagename)
                break
