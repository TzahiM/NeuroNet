#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-06-01 18:54:19
# @Author  : Weizhong Tu (mail@tuweizhong.com)
# @Link    : http://www.tuweizhong.com
import re
from xlrd import open_workbook


class OpenExcel:
    '''
    #Usage: 
    import OpenExcel
    f = OpenExcel(path) #default sheet(1) you can use `f = OpenExcel(path,sheet=2)`

    ########### read data ###########
    f.read()                               #return all data

    f.read(1) or read("1")                 # return a list of line data (horizontal)
    f.read("A")                            # return a list of column data (vertical)
    f.read('A7') or read('24A')            # return a string of special data!
    f.read("A","1")
    #you can also use read("A",1) read(1,"A") or read("1","A")
    
    ########### read sheet name ###########
    OpenExcel(path,sheet=2).readSheetName()   # return a string of sheet2 name
    f.readAllsheetsName()                      # return a list of all sheets names

    ########### getposition ###########
    f.getPosition("tuweizhong")#default completeMatch=False,stripOn=False #find a string position in excel
    #for examples:
    OpenExcel("/home/tu/tu.xls").getPosition("3D")#default completeMatch=False,stripOn=False
    OpenExcel("/home/tu/tu.xls").getPosition("3D",completeMatch=True,stripOn=True) or ("3D",1,1)
    '''

    def __init__(self, path, sheet=0, mode="r"):
        self.path = path
        self.mode = mode
        if mode == "r":
            self.data = open_workbook(path)
            self.sheets = self.data.sheet_by_index(sheet)

    def __toNum(self, args):
        if len(args) == 1:
            return (ord(args.upper())-ord("A"))
        if len(args) == 2:
            return ((ord(args[0].upper())-ord("A") + 1)*26 +  (ord(args[1].upper())-ord("A"))) #AA means 26

    def __hasChar(self, args):
        if re.compile('[a-zA-Z]').search(str(args)):
            return True
        return False

    def __hasNum(self, args):
        if re.compile('[0-9]').search(str(args)):
            return True
        return False

    '''
    #=================================
    #      A     B     C     D     E  
    #  1 (0,0) (0,1) (0,2) (0,3) (0,4)
    #  2 (1,0) (1,1) (1,2) (1,3) (1,4)
    #  3 (2,0) (2,1) (2,2) (2,3) (2,4)
    #=================================
    # (row,col)
    '''

    def _convert(self, args):
        '''convert '(1,1)' to 'B2' and 'B2' to '(1,1)' auto-recongnize'''
        if args.find(",") > -1:
            b, a = args.replace("(", "").replace(")", "").split(",")
            a = chr(int(a)+65)#chr(65) is "A" and ord("A") is 65
            b = str(int(b)+1)
            return a+b
        else:
            a = str(int(args[1:2])-1)               # D1-->(0,3)   1-->0
            b = str(ord(args[0:1].upper())-65)      # D1-->(0,3)   D-->3       ord("D") is 68
            return "("+a+","+b+")"

    def getRows(self):
        return self.sheets.nrows

    def getCols(self):
        return self.sheets.ncols

    def read(self, *args):
        if len(args) == 0:
            return self.sheets

        elif len(args) == 1:# read('A') or read('10') or read('A3')
            #1. judge read a line or a position
            args = str(args[0])
            if self.__hasChar(args) and self.__hasNum(args):# contains char and num ,such as "A5"
                # read('A3')
                _char = ''.join(re.compile('[a-zA-Z]').findall(args))
                _num = ''.join(re.compile('[0-9]').findall(args))
                return self.read(_char, _num)


            # read('A') or read('10')
            if self.__hasNum(args):# read('10')
                return self.sheets.row_values(int(args)-1)
            else:# read('A')
                return self.sheets.col_values(self.__toNum(args))

        elif len(args) == 2:#read a given position, such as read("A",10)
            if self.__hasNum(args[1]):
                b = self.__toNum(args[0])
                a = int(args[1])-1
            else:
                a = int(args[0])-1
                b = int(self.__toNum(args[1]))

            return self.sheets.cell(a, b).value
