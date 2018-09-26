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
        codeEndIndex = -1
        codeStartIndex = -1  # 有内容字符开始的地方
        for s in line:
            codeEndIndex = codeEndIndex + 1
            if s != " " and s != "\t" and codeStartIndex == -1:
                codeStartIndex = codeEndIndex

            if s == '/':
                return codeEndIndex, codeStartIndex
            elif s == "*":
                return codeEndIndex, codeStartIndex

        return codeEndIndex, codeStartIndex

    def parseJavaLine(self, line: str):
        codeEndIndex, codeStartIndex = self.checkLineCommentIndex(line)
        if codeEndIndex == -1:
            return line
        elif codeStartIndex == codeEndIndex:  # 没代码内容
            return line
        else:  # 前面是代码，后部分是注释
            comment = line[codeEndIndex:]
            code = line[codeStartIndex:codeEndIndex]
            emptyStr = line[0:codeStartIndex]
            if self.checkIsClassLine(code):
                return line
            elif self.checkIsProtertyLine(code):
                code = self.parseJavaProperty(code)
            return emptyStr + code + comment

    def parseJavaProperty(self, code: str):
        code = code.replace('  ', ' ', -1)
        code = code.replace(';', '')
        arr = code.split(' ')
        prop = Property(arr)
        return 'public var ' + prop.variableName + ':'+prop.type+';'  # 默认修饰符是public

    def checkIsClassLine(self, code: str):  # 检测是不是类的定义
        if code.find("Class ") > -1:
            return True
        else:
            return False

    def checkIsProtertyLine(self, code: str):
        if (code.find('public') > -1 or code.find('private') > -1 or code.find('protect') > -1) and code.find(';') > -1:
            return True
        else:
            return False


class Property(object):

    def __init__(self, values: list):
        self.accessModefier: str = values[0]  # 访问修饰符
        self.type: str = values[1]  # 类型
        self.variableName = values[2]  # 变量名

    pass
