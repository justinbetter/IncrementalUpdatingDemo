#!user/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import shutil
import subprocess
import sys

from os.path import join, dirname, realpath
from xml.etree.ElementTree import ElementTree

import time

AAPT_PATH = join(dirname(realpath(__file__)), 'aapt')
old_PATH = join(dirname(realpath(__file__)), 'old\\')
new_PATH = join(dirname(realpath(__file__)), 'new\\')
tinker_configure_original_path = join(dirname(realpath(__file__)), 'tinker_config_original.xml')
tinker_configure_path = join(dirname(realpath(__file__)), 'tinker_config.xml')
output_path = os.path.split(os.path.realpath(__file__))[0]+'\\output\\'
patch_path = os.path.split(os.path.realpath(__file__))[0]+'\\patch\\'
jar_path = os.path.split(os.path.realpath(__file__))[0]+'\\tinker-patch-cli-1.7.7.jar'

def get_patch(old_apk_path, new_apk_path):
    command = AAPT_PATH + ' dump xmlstrings   ' + old_apk_path + ' AndroidManifest.xml'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
    xmlTree = p.communicate()[0]
    splitlines = xmlTree.splitlines()
    # 获取application 下的索引
    app_index = 0
    manifest_index = 0
    for index , line in enumerate(splitlines):
        if line.endswith('manifest'):
            manifest_index = index + 1

        if line.endswith('application'):
            app_index = index + 1
            # print( 'application content: index %d  content: %s \napplicationIndex : %s' % (index,line,app_index,))

    # 切割获取包名,app类名
    manifest_split = splitlines[manifest_index].split(':')
    manifest_name = manifest_split[1].strip()
    manifest_array = manifest_name.split('.')
    manifest_class_name = manifest_array[-1]
    app_split = splitlines[app_index].split(':')
    app_class_name = app_split[1].strip()
    print manifest_class_name
    print app_class_name
    # tree = ElementTree(file='tinker_config_original.xml')
    tree = ElementTree(file=tinker_configure_original_path)
    for issue_tag in tree.getroot():
        if issue_tag.attrib['id'] == 'sign':
            if( app_class_name.startswith("com.tuyou.tsd.system")):
                issue_tag[0].set('value','tool_output/demo.keystore')
                print "sign: "+str(issue_tag[0].attrib)
                issue_tag[1].set('value','demo')
                print "sign: "+str(issue_tag[1].attrib)
                issue_tag[2].set('value','demo')
                print "sign: "+str(issue_tag[2].attrib)
                issue_tag[3].set('value','demo')
                print "sign: "+str(issue_tag[3].attrib)
                tree.write(tinker_configure_path)
            else:
                issue_tag[0].set('value', 'tool_output/demo.keystore')
                print "sign: " + str(issue_tag[0].attrib)
                issue_tag[1].set('value', 'demo')
                print "sign: " + str(issue_tag[1].attrib)
                issue_tag[2].set('value', 'demo')
                print "sign: " + str(issue_tag[2].attrib)
                issue_tag[3].set('value', 'demo.keystore')
                print "sign: " + str(issue_tag[3].attrib)
                tree.write(tinker_configure_path)


        if issue_tag.attrib['id'] == 'dex':
            loader_tag = issue_tag[4]
            print 'original application: ', loader_tag.attrib
            loader_tag.set('value', app_class_name)
            # tree.write('tinker_config.xml')
            tree.write(tinker_configure_path)

    print 'haha! xml finished! after modification applicatio: ', loader_tag.attrib
    # 调用cmd 合成patch
    # java -jar tinker-patch-cli-1.7.7.jar -old old.apk -new new.apk -config tinker_config.xml -out output
    print old_apk_path
    print new_apk_path
    command_patch = 'java -jar ' + jar_path + ' -old ' + old_apk_path + ' -new ' + new_apk_path + ' -config ' + tinker_configure_path + ' -out ' + output_path + manifest_class_name
    print command_patch
    patch_log = os.popen(
        command_patch).read()
    print patch_log
    # ,将成功的patch重命名复制到patch文件夹,完成
    if not os.path.exists(patch_path):
        os.mkdir(patch_path)

    now_time = str(int(time.time()))
    shutil.copyfile(output_path + manifest_class_name + '/patch_signed.apk',
                    patch_path + manifest_class_name + '_' + now_time + '.patch')
    os.system(
        'echo  ' + manifest_class_name + '_' + now_time + '.patch success! you can go to directory /patch find patch')
    os.system('echo haha!go!go!go!')


def get_packagename(apk):
    command_getpackagename =AAPT_PATH +" d badging " + apk
    p = subprocess.Popen(command_getpackagename, stdout=subprocess.PIPE, stderr=None, shell=True)
    p_communicate = p.communicate()
    pattern = re.compile(r'package: name=\'(\S+)\'')
    search = pattern.search(p_communicate[0])
    package_name = search.group(1)
    return package_name

if __name__ == '__main__':
    # print len(sys.argv),str(sys.argv)
    # 至少给两个apk地址
    # if len(sys.argv) <= 2:
    #     print 'parameters are not enough!'
    #     sys.exit(2)
    # 获取第一个apk 循环除了自身以外的apk，判断包名相同，安装;list remove
    # apk_old = raw_input('old_path: ')
    # apk_new = raw_input('new_path: ')
    apk_old_list = [old_PATH+f for f in os.listdir(old_PATH) ]
    apk_new_list = [new_PATH+f for f in os.listdir(new_PATH) ]

    # apk_old_list = apk_old.strip().split(' ')
    # apk_new_list = apk_new.strip().split(' ')
    print apk_old_list
    print apk_new_list
    for old_index , old_apk in enumerate(apk_old_list):
        # print index,apk
        packagename = get_packagename(old_apk)
        # print index
        for new_index, new_apk in enumerate(apk_new_list):
            second_package_name = get_packagename(new_apk)
            if second_package_name == packagename:
                # print second_index
                print 'same packagename: %s go patch' % second_package_name
                get_patch(old_apk, new_apk)
                # 删除list
                break

    os.system("pause")
