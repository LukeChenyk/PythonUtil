# -*- coding: utf-8 -*-
import os
import re
from base.IFileHandle import *
from configs import *


class GenASFileHandler(IFileHandle):

    def __init__(self):
        self.reset()
        pass

    def reset(self):
        self.hasFunLeftKuoHao = False
        self.lastPropertyLineIndex = -1
        self.curCheckLineIndex = -1
        self.classDefineLineIndex = -1
        self.typeInfo = TypeInfo()
        pass

    def handle(self, inPath: str, outPath: str, fileName: str):
        self.reset()

        infile = inPath + '/' + fileName
        if infile.find('SM_') > -1:
            self.typeInfo.isRead = True
            self.typeInfo.addImportType('Message')
        elif infile.find('CM_') > -1:
            self.typeInfo.isWrite = True
            self.typeInfo.addImportType('Message')
        else:
            self.typeInfo.addImportType('Bean')

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

        self.startWriteFile(newfp, newlines)

        if self.typeInfo.isWrite:
            self.writeWriteFunc(newfp)
            self.writeGetIdFunc(newfp)
        elif self.typeInfo.isRead:
            self.writeReadFunc(newfp)
            self.writeGetIdFunc(newfp)
        else:
            self.writeReadFunc(newfp)  # bean只需读的方法

        newfp.write('\n\t}\n}\n')

        newfp.close()

    # ***************************************************************************

    def startWriteFile(self, newfp, lines: list):
        for index, line in enumerate(lines):
            if line and index > self.lastPropertyLineIndex:  # 去掉了成员方法
                pass
            elif line:
                if index > 0:
                    line = '\t' + line
                if index == self.classDefineLineIndex:
                    self.writeImport(newfp)
                    self.writeDoc(newfp)
                newfp.write(line)
        pass

    def writeImport(self, outFile):
        for s in self.typeInfo.importTypes:
            outFile.write('\timport ' + s + ';\n')
        outFile.write('\n')
        pass

    def writeDoc(self, outFile):
        for s in Configs.FILE_DOC:
            outFile.write('\t' + s + '\n')
        pass

    # 读的方法
    def writeReadFunc(self, outFile):
        outFile.write(
            '\n\t\toverride protected function reading():Boolean {\n')

        for prop in self.typeInfo.props:
            outFile.write('\t\t\t' + prop.variableName +
                          ' = ' + prop.getReadFunc() + ';\n')
            pass
        outFile.write('\t\t\treturn true;\n')
        outFile.write('\t\t}\n')
        pass

    # 写的方法
    def writeWriteFunc(self, outFile):
        outFile.write(
            '\n\t\toverride protected function writing():Boolean {\n')

        for prop in self.typeInfo.props:
            outFile.write('\t\t\t' + prop.variableName +
                          ' = ' + prop.getWriteFunc() + ';\n')
            pass
        outFile.write('\t\t\treturn true;\n')
        outFile.write('\t\t}\n')
        pass

    def writeGetIdFunc(self, outFile):
        outFile.write('\n')
        outFile.write('\t\toverride public function getId():int {\n')
        outFile.write('\t\t\treturn -xxxx;\n')
        outFile.write('\t\t}\n')
        pass

    # ***************************************************************************

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

            elif self.checkIsImpot(code):
                return None  # 删除java的import
            else:
                return line

            return emptyStr + code + comment

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
        if Configs.Base_Import.__contains__(prop.type):
            self.typeInfo.addImportType(prop.type)
        return 'public var ' + prop.variableName + ':'+prop.getTypeName()+';'  # 默认修饰符是public

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

    def checkIsImpot(self, code: str):
        if code.find('import') > -1:
            return True
        else:
            return False


class Property(object):

    def __init__(self, values: list):
        self.reset()
        self.accessModefier: str = values[0]  # 访问修饰符
        self.type: str = self.parseType(values[1])  # 类型
        self.variableName = self.parseVariableName(values[2])  # 变量名

    def reset(self):
        self.keyBean: str = ''
        self.valueBean: str = ''
        pass

    def parseVariableName(self, variableName: str):
        if variableName[0] == '_':
            variableName = variableName[1:]
        return variableName

    def parseType(self, typeStr: str):
        if typeStr.find('Map<') == 0:
            typeStr = re.findall(r"<(.+?)>", typeStr)[0]
            typeStr = typeStr.replace('$', '')
            arr = typeStr.split(',')
            self.keyBean = self.transType(arr[0])
            self.valueBean = self.transType(arr[1])
            typeStr = 'Map'

            # return 'Object.<' + self.keyBean + ',' + self.valueBean + '>'
        elif typeStr.find('List<') == 0:
            self.type = 'Array'
            typeStr = re.findall(r"<(.+?)>", typeStr)[0]
            self.valueBean = self.transType(typeStr)
            typeStr = 'Array'
            # return 'Vector.<'+self.valueBean+'>'
        return self.transType(typeStr)

    def getTypeName(self):
        if self.type == 'Byte':
            return 'int'
        elif self.type == 'Array':
            return 'Vector.<'+self.valueBean+'>'
        elif self.type == 'Map':
            return 'Object'
        else:
            return self.type
        pass

    def transType(self, typeStr: str):
        if typeStr == 'Integer':
            return 'int'
        elif typeStr == 'boolean':
            return 'Boolean'
        elif typeStr == 'byte':
            return 'Byte'
        else:
            return typeStr
        pass

    def getReadFunc(self):
        switch = Configs.Base_Read_Func
        if switch.__contains__(self.type):
            return switch[self.type]
        if self.type == 'Array':
            return 'readArray('+self.getMapType(self.valueBean) + ', ' + self.getBeanClass(self.valueBean) + ')'
        elif self.type == 'Map':
            return 'readObject('+self.getMapType(self.keyBean) + ', '+self.getMapType(self.valueBean) + ', '+self.getBeanClass(self.keyBean) + ', ' + self.getBeanClass(self.valueBean)+')'
        else:
            return 'readBean('+self.type+')'

    def getWriteFunc(self):
        switch = Configs.Base_Write_Func
        if switch.__contains__(self.type):
            return switch[self.type]
        if self.type == 'Array':
            return 'writeArray('+self.getMapType(self.valueBean) + ', ' + self.getBeanClass(self.valueBean) + ')'
        elif self.type == 'Map':
            return 'writeObject('+self.getMapType(self.keyBean) + ', '+self.getMapType(self.valueBean) + ', '+self.getBeanClass(self.keyBean) + ', ' + self.getBeanClass(self.valueBean)+')'
        else:
            return 'writeBean('+self.type+')'
        pass

    def getMapType(self, typeStr: str):
        switch = Configs.MAP_TYPE
        if self.checkIsBaseType(typeStr):
            return switch[typeStr]
        else:
            return switch['Bean']
        pass

    def getBeanClass(self, beanName: str):
        if Property.checkIsBaseType(beanName):
            return 'null'
        return beanName

    @staticmethod
    def checkIsBaseType(typeStr):
        switch = Configs.Base_Type
        if switch.__contains__(typeStr):
            return True
        else:
            return False
        pass

    pass


class TypeInfo(object):

    def __init__(self):
        self.props = []
        self.isWrite: bool = False
        self.isRead: bool = False
        self.packageName: str = ''
        self.importTypes: list = []
        pass

    def addProperty(self, prop: Property):
        self.props.append(prop)
        pass

    def setPackage(self, name: str):
        self.packageName = name
        pass

    def addImportType(self, type):
        importStr = Configs.Base_Import[type]
        if importStr in self.importTypes:
            return

        self.importTypes.append(importStr)
        pass

    pass
