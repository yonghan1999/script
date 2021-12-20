# This is a sample Python script.

import xlrd
import argparse
import sys
import fileinput
import re

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# 需要配置 开始行号和结束行号 和 文件名
start_line = 0
end_line = 0
excel_file_name = "1.xlsx"


excel_sheet_index = None
excel_sheet_col = None
excel_sheet_col_replace = None
regex = None
file_name = None

excel_file = None
excel_sheet = None

iosKeyIndex = 2
cn = 5
en = 6
ja = 7
ko = 8
ru = 9
th = 10


def load_excel():
    global excel_file, excel_sheet, excel_sheet_index, excel_file_name
    excel_file_name = "1.xlsx"
    excel_file = xlrd.open_workbook(excel_file_name)
    excel_sheet = excel_file.sheet_by_name("三端全量文案（中文）")


def add():
    global file_name, excel_sheet, excel_sheet_col
    for i, row in enumerate(excel_sheet.get_rows()):
        iosKey = row[iosKeyIndex].value
        cnStr = row[cn].value
        enStr = row[en].value
        jaStr = row[ja].value
        koStr = row[ko].value
        ruStr = row[ru].value
        thStr = row[th].value
        if start_line <= i <= end_line and len(iosKey) > 0:
            if len(cnStr) > 0:
                print(cnStr)
                with open("zh-Hans.lproj/baseLanguage.strings", "a") as file:
                    str = "\"" + iosKey + "\" = \"" + cnStr + "\"\n"
                    file.write(str)
            if len(enStr) > 0:
                print(enStr)
                with open("en.lproj/baseLanguage.strings", "a") as file:
                    str = "\"" + iosKey + "\" = \"" + enStr + "\"\n"
                    file.write(str)
            if len(jaStr) > 0:
                print(jaStr)
                with open("ja.lproj/baseLanguage.strings", "a") as file:
                    str = "\"" + iosKey + "\" = \"" + jaStr + "\"\n"
                    file.write(str)
            if len(koStr) > 0:
                print(koStr)
                with open("ko.lproj/baseLanguage.strings", "a") as file:
                    str = "\"" + iosKey + "\" = \"" + koStr + "\"\n"
                    file.write(str)
            if len(ruStr) > 0:
                print(ruStr)
                with open("ru.lproj/baseLanguage.strings", "a") as file:
                    str = "\"" + iosKey + "\" = \"" + ruStr + "\"\n"
                    file.write(str)
            if len(thStr) > 0:
                print(thStr)
                with open("th.lproj/baseLanguage.strings", "a") as file:
                    str = "\"" + iosKey + "\" = \"" + thStr + "\"\n"
                    file.write(str)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_excel()
    add()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
