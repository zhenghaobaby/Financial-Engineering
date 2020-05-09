# Author : zhenghaobaby
# Time : 2020/3/27 11:52
# File : ExcelUDF.py
# Ide : PyCharm


import xlwings as xw

@xw.func
@xw.func
@xw.ret(expand='table')
def SplitUDF(string, delimiter):
    return string.split(delimiter)