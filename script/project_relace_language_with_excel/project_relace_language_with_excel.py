# This is a sample Python script.

import xlrd
import argparse
import sys
import fileinput
import re

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

excel_file_name = None
excel_sheet_index = None
excel_sheet_col = None
excel_sheet_col_replace = None
regex = None
file_name = None

excel_file = None
excel_sheet = None


# check options
def opts():
    global excel_file_name, excel_sheet_index, regex, file_name, excel_sheet_col, excel_sheet_col_replace
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--excel', action='store', dest='excel_file_name',
                        help='excel文件的路径')
    parser.add_argument('-s', '--sheet', action='store', dest='excel_sheet_index',
                        help='第几个sheet，从1开始')
    parser.add_argument('-c', '--col', action='store', dest='excel_sheet_col',
                        help='sheet中第几列')
    parser.add_argument('-R', '--regex', action='store', dest='regex',
                        help='正则表达式匹配规则')
    parser.add_argument('-f', '--file', action='store', dest='file_name',
                        help='目标文件的路径')
    parser.add_argument('-r', '--replace', action='store', dest='excel_sheet_col_replace',
                        help='目标文件的路径')
    parser.parse_args()
    args = parser.parse_args()
    if args.excel_file_name is None or args.excel_sheet_index is None or args.excel_sheet_col is None \
            or args.file_name is None or args.excel_sheet_col_replace is None:
        print("ERROR: parameters error!")
        sys.exit()
    else:
        excel_file_name = args.excel_file_name
        excel_sheet_index = args.excel_sheet_index
        if args.regex is not None:
            regex = args.regex
        file_name = args.file_name
        excel_sheet_col = args.excel_sheet_col
        excel_sheet_col_replace = args.excel_sheet_col_replace
    print(excel_file_name + " " + excel_sheet_index + " " + " " + file_name + " " + excel_sheet_col)


def load_excel():
    global excel_file, excel_sheet, excel_sheet_index
    excel_file = xlrd.open_workbook(excel_file_name)
    # excel_sheet = excel_file.sheet_by_index(int(excel_sheet_index))
    excel_sheet = excel_file.sheet_by_name("三端全量文案（中文）")


def replace():
    global file_name, excel_sheet, excel_sheet_col, excel_sheet_col_replace
    # index = 1
    # for row in excel_sheet.get_rows():
    #     index += 1
    #     if index > 50:
    #         break
    #     col_val = row[int(excel_sheet_col)+1].value
    #     if col_val is not None and len(col_val) is not 0:
    #         print(str(col_val))
    for line in fileinput.input(file_name, backup=".bak", inplace=True):
        # if bool(re.match(regex, line)):
        #     print(line)
        for row in excel_sheet.get_rows():
            col_val = str(row[int(excel_sheet_col) + 1].value)
            replace_val = str(row[int(excel_sheet_col_replace) + 1].value)
            # match string
            match_str = ".*\"" + col_val + "\".*"
            if col_val is not None and len(col_val) != 0 and replace_val is not None and len(replace_val) != 0:
                if bool(re.match(match_str, line)):
                    line = line.replace(col_val, replace_val)
                    break
        print(line, end="")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    opts()
    load_excel()
    replace()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
