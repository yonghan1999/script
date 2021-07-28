import argparse
import requests
import json
import xlwt
# https://restapi.amap.com/v3/geocode/regeo?key=d0b75383e16f1312ec2e019935ba8ecc&location=116.481488,39.990464&poitype=商务写字楼&radius=1000&extensions=all&batch=false&roadlevel=0
import sys

# amap_web_key = ''; you need add it before use the secript


# check options
def opts():
    location = None
    radius = 1000
    poitype = None

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--location', action='store', dest='location',
                        help='传入内容规则：经度在前，纬度在后，经纬度间以“,”分割，经纬度小数点后不要超过 6 位。'
                             '如果需要解析多个经纬度的话，请用"|"进行间隔,最多支持传入 20 对坐标点。每对点坐标之间用"|"分割。')
    parser.add_argument('-p', '--poitype', action='store', dest='poitype',
                        help='支持传入POITYPECODE及名称；支持传入多个POI类型，多值间用"｜"分隔')
    parser.add_argument('-r', '--radius', action='store', dest='radius',
                        help='查询POI的半径范围。取值范围：0～3000，单位米。默认值：1000')
    parser.parse_args()
    args = parser.parse_args()
    if (args.location is None):
        print("ERROR: You use at least the --location or -l parameter")
        sys.exit()
    else:
        location = args.location
        if args.radius is not None:
            radius = args.radius
        if args.poitype is not None:
            poitype = args.poitype
        return location, radius, poitype


# get resource
def get_res(location, radius, poitype):
    url = 'https://restapi.amap.com/v3/geocode/regeo'
    data = {
        'key': amap_web_key,
        'location': location,
        'extensions': 'all',
        'batch': 'false',
        'roadlevel': '0'
    }
    if radius is not None:
        data.update(radius=radius)
    if poitype is not None:
        data.update(poitype=poitype)
    response = requests.get(url, data)
    if response.status_code == 200:
        json_res = json.loads(response.text)
        regeocode = json_res['regeocode']
        return regeocode['pois']


def json_out_to_file(json):
    title = ["id", "name", "type", "tel", "direction", "distance", "location", "address", "poiweight", "businessarea"]
    excel = xlwt.Workbook()
    sheet = excel.add_sheet('POIS', cell_overwrite_ok=True)
    for i in range(len(title)):
        sheet.write(0, i, title[i])
    for index1, line in enumerate(json):  # 循环字典
        print('line:', line)
        for index2, val in enumerate(line.values()):
            sheet.write(index1 + 1, index2, val)
    excel.save('demo.xls')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    location, radius, poitype = opts()
    json = get_res(location, radius, poitype)
    json_out_to_file(json)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
