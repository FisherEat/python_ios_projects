#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
剔除iOS Xcode项目中没有用到的图片
'''
import csv
import codecs
import os
import re
import time
import openpyxl


def cur_file_dir():
    # 文件的当前路径
    path = os.path.split(os.path.realpath(__file__))[0]
    return path


placeholdRe = re.compile(r'\%\d{1,2}\$s(\s|\?)?')

rootPath = cur_file_dir()
# 上级目录
rootPath = os.path.dirname(rootPath)
inputFile = os.path.join(rootPath, "001.xlsx")
# inputFile = rootPath + "v6Strings.csv"
# targetPath = "E:/WorkProject/iosV6/"
# targetPath = rootPath
targetPath = os.path.join(rootPath, "SmartHomeV6/")
outputFileData = [["en.lproj/", "Localizable.strings", 1], ["zh-Hans.lproj/", "Localizable.strings", 2]]


def getLocalizedStringFile():
    for outputFile in outputFileData:
        targetFilePath = targetPath + outputFile[0]
        targetFile = targetFilePath + outputFile[1]
        column_index = outputFile[2]
        if not os.path.exists(targetFilePath):
            os.makedirs(targetFilePath)
        with codecs.open(targetFile, 'w', "utf-8") as out:
            out.write('//  %s' % time.strftime('%Y-%m-%d %H:%M:%S'))
            s = 0
            # csv_reader = csv.reader(open(inputFile, encoding='utf-8'))
            xlxs = openpyxl.load_workbook(inputFile, read_only=True)
            wb = xlxs.active
            contentArr = []
            for row in wb.rows:
                # 0 第1列分组  1 第5列英文  2 第4列中文  3 第2列Key
                s += 1
                if s == 1:
                    continue
                contentArr.append([row[1].value, row[5].value, row[4].value, row[2].value])
            contentArr.sort(key= lambda x:x[0].lower())


            groupName = ''
            for row in contentArr:
                
                if groupName != row[0]:
                    out.write('\n\n' + '/* %s */' % row[0] + '\n')
                    groupName = row[0]

                targetStr = row[column_index]
                if targetStr == None:
                    targetStr = ""
                if not isinstance(targetStr, str):
                    targetStr = str(targetStr)
                if targetStr.find('\"') > 0 or targetStr.startswith('\"'):
                    targetStr = targetStr.replace('\"', '\\\"')

                if targetStr.find('\n') > 0:
                    targetStr = targetStr.replace('\n', '\\n')

                targetStr = placeholdRe.sub('%@', targetStr)

                out.write("\"%s=   \"%s\";" % ((row[3].replace('\n', '') + "\"").ljust(60), targetStr))
                out.write("\n")
            out.flush()

# if __name__ == '__main__':
#     getLocalizedStringFile()