#!user/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
from os.path import join, dirname, realpath
import hashlib
import json
import re
import time


# 获取包名
import shutil

# bsdiff.exe目录
old_PATH = join(dirname(realpath(__file__)), 'old\\')
new_PATH = join(dirname(realpath(__file__)), 'new\\')
patch_PATH = join(dirname(realpath(__file__)), 'patch\\')
bspatch_PATH = join(dirname(realpath(__file__)), 'bspatch')
# patch_apk所在目录
patch_apk_dst_path = os.path.split(os.path.realpath(__file__))[0] + '\\patch_new\\'

def get_packagename(apk):
    command_getpackagename = "aapt d badging " + apk
    p = subprocess.Popen(command_getpackagename, stdout=subprocess.PIPE, stderr=None, shell=True)
    p_communicate = p.communicate()
    pattern = re.compile(r'package: name=\'(\S+)\'')
    search = pattern.search(p_communicate[0])
    package_name = search.group(1)
    return package_name


# 简单的测试一个字符串的MD5值
def GetStrMd5(src):
    m0 = hashlib.md5()
    m0.update(src)
    print m0.hexdigest()
    pass


# 大文件的MD5值
def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = file(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


def CalcSha1(filepath):
    with open(filepath, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        print(hash)
        return hash


def CalcMD5(filepath):
    with open(filepath, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        print(hash)

# 根据patchs生成apk
def get_patch_apk(old_apk, old_patch, packagename):
    packagename_split = packagename.split('.')
    packagename_end = packagename_split[-1]
    now_time = str(int(time.time()))
    patch_apk_name = packagename_end + now_time + '.apk'
    command_patch = bspatch_PATH + ' ' + old_apk + ' ' + patch_apk_name + ' ' + old_patch
    print command_patch
    patch_log = os.popen(
        command_patch).read()
    print patch_log

    # 移动patch
    if not os.path.exists(patch_apk_dst_path):
        os.mkdir(patch_apk_dst_path)

    shutil.move(patch_apk_name, patch_apk_dst_path + patch_apk_name)
    os.system('echo haha!go!go!go!')



if __name__ == '__main__':

    #apk_old = raw_input('old_path: ')
    #apk_new = raw_input('new_path: ')
    apk_old_list = [old_PATH + f for f in os.listdir(old_PATH)]
    apk_patch_list = [patch_PATH + f for f in os.listdir(patch_PATH)]

    #apk_old_list = apk_old.strip().split(' ')
    #apk_new_list = apk_new.strip().split(' ')
    # print apk_old_list
    # print apk_patch_list
    for old_index, old_apk in enumerate(apk_old_list):
        # print index,apk
        packagename = get_packagename(old_apk)
        # print index
        for new_index, old_patch in enumerate(apk_patch_list):
            packagename_split = packagename.split('.')
            packagename_end = packagename_split[-1]
            if(packagename_end in old_patch):
                # print second_index
                print 'same packagename:%s ---- find-----%s=================== go patch' %(packagename_end, old_patch)
                get_patch_apk(old_apk, old_patch, packagename)
                break

    # 输出MD5
    apk_new_list = [new_PATH+f for f in os.listdir(new_PATH) ]
    apk_patch_apk_list = [patch_apk_dst_path + f for f in os.listdir(patch_apk_dst_path)]
    print "=======after patch finish ========================="
    for newApk in apk_new_list:
        packagename = get_packagename(newApk)
        packagename_split = packagename.split('.')
        packagename_end = packagename_split[-1]
        for patchIndex,patchApk in enumerate(apk_patch_apk_list):
            if(packagename_end in patchApk):
                print "%d new apk md5 : %s , patch apk md5 : %s " % (patchIndex+1, GetFileMd5(newApk),GetFileMd5(patchApk))

    os.system("pause")
