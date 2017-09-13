import hashlib
import os
import re
import shutil
import subprocess
import time
from os.path import join, dirname, realpath
from xml.etree.ElementTree import ElementTree

# 目录
AAPT_PATH = join(dirname(realpath(__file__)), 'aapt')
old_PATH = join(dirname(realpath(__file__)), 'old\\')
new_PATH = join(dirname(realpath(__file__)), 'new\\')
patch_PATH = join(dirname(realpath(__file__)), 'patch\\')
bspatch_PATH = join(dirname(realpath(__file__)), 'bspatch')
# patch_apk所在目录
patch_apk_dst_path = os.path.split(os.path.realpath(__file__))[0] + '\\patch_new\\'
# tinker
tinker_configure_original_path = join(dirname(realpath(__file__)), 'tinker_config_original.xml')
tinker_configure_path = join(dirname(realpath(__file__)), 'tinker_config.xml')
output_path = os.path.split(os.path.realpath(__file__))[0] + '\\output\\'
patch_path = os.path.split(os.path.realpath(__file__))[0] + '\\patch\\'
jar_path = os.path.split(os.path.realpath(__file__))[0] + '\\tinker-patch-cli-1.7.7.jar'


class CommonUtils:
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
    def get_patch_apk(bspatch_PATH, old_apk, old_patch, packagename):
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
        # if not os.path.exists(patch_apk_dst_path):
        #     os.mkdir(patch_apk_dst_path)
        #
        # shutil.move(patch_apk_name, patch_apk_dst_path + patch_apk_name)
        # os.system('echo haha!go!go!go!')

    def get_patch(old_apk_path, new_apk_path):
        command = AAPT_PATH + ' dump xmlstrings   ' + old_apk_path + ' AndroidManifest.xml'
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        xmlTree = p.communicate()[0]
        splitlines = xmlTree.splitlines()
        # 获取application 下的索引
        app_index = 0
        manifest_index = 0
        for index, line in enumerate(splitlines):
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
