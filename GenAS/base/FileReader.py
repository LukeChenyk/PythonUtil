#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from base.IFileHandle import *
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


class FileReader(object):

    def __init__(self, fileHandler: IFileHandle):
        self.fileHandler: IFileHandle = fileHandler
        pass

    '''
    '' 打印一个目录下的所有文件夹和文件
    '''

    def handleFiles(self, inPath, outPath):
        allFileNum = 0

        dirList = []
        fileList = []
        files = os.listdir(inPath)
        # dirList.append(str(level))

        for f in files:
            inFile = inPath + '/' + f
            outFile = outPath + "/" + f
            if os.path.isdir(inFile):
                # 排除隐藏文件夹。因为隐藏文件夹过多
                if f[0] == '.':
                    pass
                else:
                    # 添加非隐藏文件夹
                    dirList.append(f)

            if os.path.isfile(inFile):
                self.fileHandler.handle(inFile, outFile)

        for dl in dirList:
            self.handleFiles(inPath + '/' + dl, outPath+"/"+dl)
