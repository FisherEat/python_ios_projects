
import os
import matplotlib.pyplot as plt
from PIL import Image
import numpy
import shutil
#dir = '/Users/mini5/Desktop/V6 瘦身/sceneIcon'
# dir = '/Users/mini5/Desktop/work/SmartHomeV6Code_IOS/SmartHomeV6/Resource/v6Html'
dir = '/Users/gl/SmartHomeV6Code_IOS/SmartHomeV6/Assets.xcassets'
dir = '/Users/gl/SmartHomeV6Code_IOS'

files = []
imgs = []

imagesText=open('imgsPath.txt','w',encoding="utf-8")
allFileText=open('allFilePath.txt','w', encoding="utf-8")

xlabels = ["小于1k",'1-10k','10-20k','20-50k','50-100k','大于100k']
classify1 = []
classify10 = []
classify20 = []
classify50 = []
classify100 = []
classifymore100 = []


# 查找所有文件
def searchDirFile(dir):
    global filelist
    listfile = os.listdir(dir)
    filepath = dir
    for file in listfile:  # 把目录下的文件都赋值给line这个参数
        if os.path.isdir(filepath + "/" + file):
            searchDirFile(filepath + '/' + file)
        else:
            fileAllPath = os.path.join(filepath,file)
            files.append(fileAllPath)

            allFileText.write(fileAllPath + '\n')
            if file.endswith(".png") or file.endswith(".PNG") or file.endswith(".jpg") or file.endswith(".jpeg"):
                imgs.append(fileAllPath)
                imagesText.write(fileAllPath + '\n')

#给图片资源分类
def classifyImgs(images):
    for file in images:
        fileSizeClassify(file)

#根据路径划分大小
def fileSizeClassify(file):
    fileSize = os.path.getsize(file)
    if fileSize < 1024:
        #小于1k
        classify1.append(file)
    elif fileSize < 1024 * 10:
        # 小于10k
        classify10.append(file)
    elif fileSize < 1024 * 20:
        # 小于20k
        classify20.append(file)
    elif fileSize < 1024 * 50:
        # 小于50k
        classify50.append(file)
    elif fileSize < 1024 * 100:
        # 小于100k
        classify100.append(file)
    else:
        #大于100k
        classifymore100.append(file)

def createBar():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    plt.figure(figsize = (8,6))
    x = range(0,len(xlabels))
    y = [len(classify1),len(classify10),len(classify20),len(classify50),len(classify100),len(classifymore100),]
    plt.bar(x,y,width = 0.3, color = 'g')
    plt.ylabel('图片数量')
    plt.xlabel('图片大小')
    plt.title('V6 iOS工程图片大小')
    plt.xticks(range(0,len(xlabels)),xlabels)

    for a, b in zip(x, y):
        plt.text(a, b + 0.5, '%.0f' % b, ha='center', va= 'bottom',fontsize=7)

    plt.legend()
    plt.show()

#替换超过100k的图片
def replaceProjectImages():
    for file in classifymore100:
        try:
            print(file)
            fileName = os.path.basename(file)
            #替换的源文件
            sourceFilePath = '/Users/gl/Desktop/imgs/' + fileName
            # 拷贝到指定目录
            shutil.copy(sourceFilePath, file)
        except:
            continue


#获取超过100k图片
def getProjectImages():
    for file in classifymore100:
        # 拷贝到指定目录
        shutil.copy(file, '/Users/gl/Desktop/v6slim/imgs')
        print(file + '     大小 %.0f k' % ((os.path.getsize(file)) / 1024.0) + '\n')


if __name__ == '__main__':
    searchDirFile(dir)
    classifyImgs(imgs)
    getProjectImages()
    print('图片数量：%d' % len(classifymore100))
    # replaceProjectImages()
    createBar()
