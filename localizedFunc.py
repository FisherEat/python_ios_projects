#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
strPattern = re.compile(r'@\"(.*?)(?<!\\)\"')

def cur_file_dir():
    # python虚拟机的打开路径
    path = sys.path[0]

    # 改为上级目录
    if os.path.isdir(path):
        # return path
        return os.path.dirname(path)
    elif os.path.isfile(path):
        # return os.path.dirname(path)
        dir = os.path.dirname(path)
        return os.path.dirname(dir)

def outPutlogFile(str):
    strings = restringTostring(str)
    rootPath = cur_file_dir()
    logfile = os.path.join(rootPath, 'log.txt')
    with open(logfile, 'a', encoding='utf-8') as f:
        f.write(strings)

# localStingPath = os.path.join(cur_file_dir(), 'Localizable.strings')
localStingPath = os.path.join(cur_file_dir(), 'SmartHomeV6/zh-Hans.lproj/Localizable.strings')

def findkeyforstring(string):
    key = ''
    restr = r'"(\w+)"\s*=\s*"%s";'%(string)
    with open(localStingPath, 'r', encoding='utf-8') as f:
        text = f.read()
        match = re.search(restr, text)
        if match != None:
            key = match.group(1)
    return key

def findstringforkey(en):
    string = None
    restr = r'"%s"\s*=\s*"(.*)";'%(en)
    with open(localStingPath, 'r', encoding='utf-8') as f:
        text = f.read()
        match = re.search(restr, text)
        if match != None:
            string = match.group(1)
    return string

global isneedwrite
global tempfilelines

def dealwithChinese(string, line):
    global tempfilelines
    global isneedwrite
    key = findkeyforstring(string)
    if key == '':
        if re.search(r'NSLog\s*\(\s*@"%s"'%string, line) != None:
            string = 'NSLog'.ljust(30) + string
            # outPutlogFile(string + "\n")
        else:
            outPutlogFile('not find Key'.ljust(30) + string + "\n")
        print(string)
    else:
        isneedwrite = 1
        if re.search(r'NSLog\s*\(\s*@"%s"'%string, line):
            print('pass')
        elif re.search(r'NSLocalizedString\s*\(\s*@"%s"\s*,\s*([\w\s]+)\s*\)'%string, line) != None:
            temp = re.sub(r'NSLocalizedString\s*\(\s*@"%s"\s*,\s*([\w\s]+)\s*\)'%string, r'NSLocalizedString(@"%s", \1)'%key, line)
            tempfilelines.pop()
            tempfilelines.append(temp)
            outPutlogFile(string.ljust(30)+ "modify :   " +key + "\n")
        elif re.search(r'@"%s"'%string, line) != None:
            temp = re.sub(r'@"%s"' % string, 'NSLocalizedString(@"%s", nil)' % key, line)
            tempfilelines.pop()
            tempfilelines.append(temp)
            outPutlogFile(string.ljust(30) + "modify :   " + key + "\n")
        else:
            print('not need')


def dealwithEnglish(string, line):
    if re.search(r'NSLocalizedString\s*\(\s*@"%s"\s*,\s*([\w\s]+)\s*\)' % string, line) != None:
        result = findstringforkey(string)
        if result == None:
            outPutlogFile(string + "\n")

def stringTorestring(string):
    string = string.replace('\\', '\\\\')
    string = string.replace('.', '\.')
    string = string.replace('(', '\(')
    string = string.replace(')', '\)')
    string = string.replace('[', '\[')
    string = string.replace(']', '\]')
    string = string.replace('{', '\{')
    string = string.replace('}', '\}')
    string = string.replace('*', '\*')
    string = string.replace('+', '\+')
    string = string.replace('?', '\?')
    string = string.replace('^', '\^')
    string = string.replace('$', '\$')
    return string


def restringTostring(string):
    string = string.replace('\\\\', '\\')
    string = string.replace('\.', '.')
    string = string.replace('\(', '(')
    string = string.replace('\)', ')')
    string = string.replace('\[', '[')
    string = string.replace('\]', ']')
    string = string.replace('\{', '{')
    string = string.replace('\}', '}')
    string = string.replace('\*', '*')
    string = string.replace('\+', '+')
    string = string.replace('\?', '?')
    string = string.replace('\^', '^')
    string = string.replace('\$', '$')
    return string

if __name__ == '__main__':
    print('shit')
    print(restringTostring("'hahg\asdlfj.skdjfl/8/'"))

#
# if __name__ == '__main__':
#     xlxs2ios.getLocalizedStringFile()
#     global isneedwrite
#     isneedwrite = 0
#     global tempfilelines
#     tempfilelines = []
#     print(cur_file_dir())
#     cur_Path = cur_file_dir()
#     for root, dirs, files in os.walk(cur_Path):
#         if root.find("Pods/") < 0 and root.find("Libs/") < 0:
#             for file in files:
#                 if file.endswith(".m"):
#                     mfile = os.path.join(root, file)
#                     if os.path.isfile(mfile):
#                         with open(mfile, 'r', encoding='utf-8') as f:
#                             tempfilelines = []
#                             for line in f.readlines():
#                                 tempfilelines.append(line)
#                                 for string in strPattern.findall(line):
#
#                                         if zhPattern.search(string):
#                                             print(line)
#                                             print('{}\n'.format(string))
#                                             try:
#                                                 newstring = stringTorestring(string)
#                                                 # newstring = string
#                                                 dealwithChinese(newstring, line)
#                                             except:
#                                                 print("Unexpected error:", sys.exc_info()[0])
#                                                 dealwithChinese(string, line)
#                                                 # newstring = stringTorestring(string)
#                                                 # dealwithChinese(newstring, line)
#                                         else:
#                                             print('{}\n'.format(string))
#                                             try:
#                                                 newstring = stringTorestring(string)
#                                                 # newstring = string
#                                                 dealwithEnglish(newstring, line)
#                                             except:
#                                                 print("Unexpected error:", sys.exc_info()[0])
#                                                 dealwithEnglish(string, line)
#                                                 # newstring = stringTorestring(string)
#                                                 # dealwithEnglish(newstring, line)
#
#                         if isneedwrite == 1:
#                             with open(mfile, 'w', encoding='utf-8') as f:
#                                 f.writelines(tempfilelines)
