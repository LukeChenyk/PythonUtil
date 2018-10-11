# -*- coding: utf-8 -*-
import os
from base.IFileHandle import *

fileDoc = ["/**", " * AutoGen", " */"]


class GenASFileHandler(IFileHandle):

    def __init__(self):
        self.reset()
        pass

    def reset(self):
        self.hasFunLeftKuoHao = False
        self.lastPropertyLineIndex = -1
        self.curCheckLineIndex = -1
        self.classDefineLineIndex = -1
        self.isRead = True
        self.typeInfo = TypeInfo()
        pass

    def handle(self, inPath: str, outPath: str, fileName: str):
        self.reset()

        infile = inPath + '/' + fileName
        if infile.find('SM_') > -1:
            self.isRead = True
        else:
            self.isRead = False

        oldlines = open(infile, encoding='utf-8').readlines()

        newlines = []
        for s in oldlines:
            newlines.append(self.parseJavaLine(s))

        path = outPath + '/' + self.typeInfo.packageName
        if not os.path.exists(path):
            os.makedirs(path)

        outFile = path + '/' + fileName
        outFile = outFile.replace('.java', '.as')  # 更改后缀
        newfp = open(outFile, 'w', encoding='utf-8')

        self.writeDoc(newfp)

        for index, line in enumerate(newlines):
            if line and index <= self.lastPropertyLineIndex:  # 去掉了成员方法
                newfp.write(line)

        self.writeReadFunc(newfp)
        newfp.write('\n\t}\n}\n')

        newfp.close()

    def writeDoc(self, outFile):
        for s in fileDoc:
            outFile.write(s + '\n')

    def writeReadFunc(self, outFile):
        outFile.write(
            '\n\t\toverride protected function reading():Boolean {\n')

        for prop in self.typeInfo.props:
            outFile.write('\t\t\t' + prop.variableName +
                          ' = ' + prop.getReadFunc() + ';\n')
            pass
        outFile.write('\t\t\treturn true;\n')
        outFile.write('\t\t}\n')

    def parseJavaLine(self, line: str):
        self.curCheckLineIndex = self.curCheckLineIndex + 1
        codeEndIndex, codeStartIndex = self.checkLineCommentIndex(line)
        if codeEndIndex == -1:
            return line
        elif codeStartIndex == codeEndIndex:  # 没代码内容
            if self.classDefineLineIndex == -1:
                return None
            return line
        else:  # 前面是代码，后部分是注释
            comment = line[codeEndIndex:]
            code = line[codeStartIndex:codeEndIndex]
            emptyStr = line[0:codeStartIndex]
            if self.checkIsPackageLine(code):
                code = self.parsePackage(code)
            elif self.checkIsClassLine(code):
                code = self.parseClass(code)
                self.classDefineLineIndex = self.curCheckLineIndex  # 类名所在的行
            elif self.checkIsProtertyLine(code):
                code = self.parseJavaProperty(code)
                self.lastPropertyLineIndex = self.curCheckLineIndex
            elif self.checkIsFuntionLine(code):
                self.parseJavaFunction(code)
                return line
            else:
                return line

            return '\t'+emptyStr + code + comment

    # ***************************************************************************

    def parseClass(self, code: str):
        code = code.replace('{', '')
        return code + ' extends Message {'
        pass

    def parseJavaProperty(self, code: str):
        code = code.replace('  ', ' ', -1)  # 两个空格全部替换成一个空格
        code = code.replace(', ', ',$', -1)  # 处理map
        code = code.replace(';', '')
        arr = code.split(' ')
        prop = Property(arr)
        self.typeInfo.addProperty(prop)
        return 'public var ' + prop.variableName + ':'+prop.type+';'  # 默认修饰符是public

    def parseJavaFunction(self, code: str):
        pass

    def parsePackage(self, code: str):
        code = code.replace('  ', ' ', -1)  # 两个空格全部替换成一个空格
        arr = code.split(' ')
        arr2 = arr[1].split('.')
        self.typeInfo.setPackage(arr2[-2])  # 取倒数第二个为包名
        return 'package com.protocol.' + self.typeInfo.packageName + ' {\n'

    # ***************************************************************************

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

    def checkIsPackageLine(self, code: str):  # 检测是不是包的定义
        if code.find("package ") > -1:
            return True
        else:
            return False

    def checkIsClassLine(self, code: str):  # 检测是不是类的定义
        if code.find("public class ") > -1:
            return True
        else:
            return False

    def checkIsProtertyLine(self, code: str):
        if self.checkIsMember(code) and code.find(';') > -1:
            return True
        else:
            return False

    def checkIsFuntionLine(self, code: str):
        if self.checkIsMember(code) and code.find('(') > -1 and code.find('=') == -1:
            return True
        else:
            return False

    def checkIsMember(self,  code: str):
        if code.find('public') > -1 or code.find('private') > -1 or code.find('protect') > -1:
            return True
        else:
            return False


class Property(object):

    def __init__(self, values: list):
        self.accessModefier: str = values[0]  # 访问修饰符
        self.type: str = self.parseType(values[1])  # 类型
        self.variableName = self.parseVariableName(values[2])  # 变量名

    def parseVariableName(self, variableName: str):
        if variableName[0] == '_':
            variableName = variableName[1:]
        return variableName

    def parseType(self, typeStr: str):
        if typeStr.find('Map') == 0:
            return 'Object'
        elif typeStr == 'boolean':
            return 'Boolean'
        return typeStr

    def getReadFunc(self):
        switch = {'int': 'readInt()',
                  'String': 'readString()',
                  'long': 'readLong()',
                  'Boolean': 'readBoolean()'
                  }
        if switch.__contains__(self.type):
            return switch[self.type]
        return 'readObject()'

    pass


class TypeInfo(object):

    def __init__(self):
        self.props = []
        self.isWrite: bool = True  # 默认为读
        self.packageName = ''
        pass

    def addProperty(self, prop: Property):
        self.props.append(prop)
        pass

    def setPackage(self, name: str):
        self.packageName = name
        pass

    pass
