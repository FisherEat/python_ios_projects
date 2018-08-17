from PIL import Image
import math
import operator
from functools import reduce
import shutil
import os
import simplejson

path = '/Users/mini5/Desktop/work/SmartHomeV6Code_IOS/SmartHomeV6/Resource/v6Html'
#所有图片的路径
imgPaths = []

#存储有相同图片的key:imgName,value:[imgPath]
samePictureDic = {}

count = 0


# 查找所有文件
def searchDirFile(dir):
    listfile = os.listdir(dir)
    filepath = dir
    for file in listfile:  # 把目录下的文件都赋值给line这个参数
        if os.path.isdir(filepath + "/" + file):
            searchDirFile(filepath + '/' + file)
        else:
            fileAllPath = os.path.join(filepath,file)
            if file.endswith(".png") or file.endswith(".PNG") or file.endswith(".jpg") or file.endswith(".jpeg"):
                imgPaths.append(fileAllPath)


def compareImages():
    global count
    #临时存储
    tempImgs = imgPaths[:]
    for i in range(0,len(imgPaths) - 1):
        if len(imgPaths) < 1:
            return
        #要比较的图片
        img1Path = imgPaths[i]
        print("\n\n\n现在进行到:%d *****图片路径:%s\n"%(i,img1Path))

        #是否有相同图片
        samed = False
        #存储相同图片路径
        samePaths = []
        if img1Path in tempImgs:
            # 从临时数组中删除
            tempImgs.remove(img1Path)

        if len(tempImgs) > 1:
            for j in range(0,len(tempImgs)):
                # print(j)
                #对比的图片
                img2Path = tempImgs[j]
                if img1Path != img2Path:
                    if compareImage(img1Path,img2Path):
                        # print("相同")
                        #图片相同
                        samed = True
                        #添加相同图片路径
                        samePaths.append(img2Path)
                    else:
                        pass
                        # print("不相同")



        if samed:
            # print('yes')
            #有相同图片添加图片1的路径
            print("相同图片的路径")
            samePaths.append(img1Path)
            print(samePaths)
            count += 1
            print(len(samePaths))
            fileName = os.path.basename(img1Path)
            names = fileName.split(".")
            imgName = '%s%d' % (names[0], count)
            for k in range(0,len(samePaths)):
                print(k)
                path = samePaths[k]
                # 目录源文件
                sourceFilePath = '/Users/mini5/Desktop/V6 瘦身/图片比较/%s_%d.png' % (names[0], k)
                # 拷贝到指定目录
                shutil.copy(path, sourceFilePath)
                #存储到json中
                samePictureDic[imgName] = samePaths
                if path in tempImgs:
                    #从临时数组中删除
                    tempImgs.remove(path)
        else:
            print("没有相同图片")

    #遍历完毕，把json写入文件
    imagesText = open('/Users/mini5/Desktop/V6 瘦身/图片比较/TheSamePicure.json', 'w')
    str = simplejson.dumps(samePictureDic)
    imagesText.write(str + '\n')


#比较两个图片是否一样
def compareImage(img1,img2):
    image1 = Image.open(img1)
    image2 = Image.open(img2)

    print(img2)
    # 把图像对象转换为直方图数据，存在list h1、h2 中
    h1 = image1.histogram()
    h2 = image2.histogram()

    # result的值越大，说明两者的差别越大；如果result=0,则说明两张图一模一样
    result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
    if (result < 0.001):
        # print('相同')
        return True
    else:
        return False

if __name__ == '__main__':
    searchDirFile(path)
    print("共有多少图片%d" % (len(imgPaths)))
    compareImages()
