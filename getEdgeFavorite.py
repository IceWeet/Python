#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re

favoritesPath= r'C:\Users\Administrator\AppData\Local\Packages\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\RoamingState' # edge收藏夹json文件存放位置
urlPath = r'E:\BackUp\Desktop' # 存放导出的url文件的位置

# 从字符串获取合法的文件名
def getFileName(str):
	rstr = r'[\/\\\:\*\?\"\<\>\|]'
	fileName = re.sub(rstr, '_', str)
	return fileName

# 从edge浏览器收藏夹的json文件中获取每一个网址的目录及url
def getFavoritePath(fileName):
    favoritePath = None
    if os.path.splitext(fileName)[1] == '.json':
        with open(fileName, 'r', encoding='utf-8') as f:
            s = json.load(f)
            if not s['IsFolder']:
                favoritePath = ['',s['Title'],s['URL']]
                ParentId = s['ParentId']
                mybool = True
                while mybool:
                    with open(favoritesPath + '\\' + ParentId + '.json', 'r', encoding='utf-8') as f1:
                        s1 = json.load(f1)
                        favoritePath[0] = s1['Title'] + '\\' + favoritePath[0]
                        ParentId = s1['ParentId']
                        if s1['Title'] == '_Favorites_Bar_':
                            mybool = False
                favoritePath[0] = urlPath + '\\' + favoritePath[0]
    return favoritePath

# 创建url快捷方式
def createUrl(createPath,url):
    f = open(createPath,'w',encoding='utf-8')
    f.write('[InternetShortcut]\nURL=' + url)

os.chdir(favoritesPath)
for filename in os.listdir():
    favoritePath = getFavoritePath(filename)
    if favoritePath:
        if os.path.isdir(favoritePath[0]):
            pass
        else:
            os.makedirs(favoritePath[0])
        favoritePath[1] = getFileName(favoritePath[1])
        print(favoritePath[0] + favoritePath[1] + '.url', favoritePath[2],filename)
        createUrl(favoritePath[0] + favoritePath[1] + '.url', favoritePath[2])
