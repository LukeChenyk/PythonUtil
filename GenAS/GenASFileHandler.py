# -*- coding: utf-8 -*-
import os
from base.IFileHandle import *

fileDoc = ["/**", " * AutoGen", " */"]


class GenASFileHandler(IFileHandle):

    def __init__(self):
        pass

    def handle(self, infile, outFile: str):
        oldlines = open(infile, encoding='utf-8').readlines()
        outFile = outFile.replace('.java', '.as')  # 更改后缀
        newfp = open(outFile, 'w', encoding='utf-8')

        self.writeDoc(newfp)
        for s in oldlines:
            newfp.write(self.parseJavaLine(s))

        newfp.close()

    def writeDoc(self, outFile):
        for s in fileDoc:
            outFile.write(s + '\n')

    # 检测这行是不是注释

    def checkLineCommentIndex(self, line: str):
        commentStartIndex = -1
        frontNotEmptyIndex = 0  # 有内容字符开始的地方
        for s in line:
            commentStartIndex = commentStartIndex + 1
            if s == '/':
                return commentStartIndex, frontNotEmptyIndex
            elif s == "*":
                return commentStartIndex, frontNotEmptyIndex
            elif s != " " and s != "\t":
                frontNotEmptyIndex = commentStartIndex

        return commentStartIndex, frontNotEmptyIndex

    def parseJavaLine(self, line: str):
        commentIndex, frontNotEmptyIndex = self.checkLineCommentIndex(line)
        if commentIndex == -1:
            return line
        elif frontNotEmptyIndex == commentIndex:  # 整行都是注释
            return line
        else:  # 前面是代码，后部分是注释
            comment = line[commentIndex:]
            code = line[frontNotEmptyIndex:commentIndex]
            emptyStr = line[0:frontNotEmptyIndex]
            return emptyStr+code+comment


class Property(object):

    def __init__(self):
        pass

    def funcname(self, parameter_list):
        pass

    pass
