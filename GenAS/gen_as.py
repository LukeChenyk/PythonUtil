#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from base.FileReader import *
from GenASFileHandler import *


def main():
    fileHandler = GenASFileHandler()
    freader = FileReader(fileHandler)
    freader.handleFiles("./GenAS/java", "./GenAS/as")
    pass


if __name__ == '__main__':
    main()
