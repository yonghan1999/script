# -*- coding: utf8 -*-

import requests
import json
import time
import random

# 填写cookie即可运行
'''
1、浏览器登入哔哩网站
2、访问 http://api.bilibili.com/x/space/myinfo
3、F12看到cookie的值粘贴即可
'''
cookies = ""


# cookie转字典
def extract_cookies(cookies):
    global csrf
    cookies = dict([l.split("=", 1) for l in cookies.split("; ")])
    csrf = cookies['bili_jct']
    return cookies


# 银币数
def getCoin():
    cookie = extract_cookies(cookies)
    url = "http://account.bilibili.com/site/getCoin"
    r = requests.get(url, cookies=cookie).text
    j = json.loads(r)
    money = j['data']['money']
    return int(money)


# 个人信息
def getInfo():
    global uid
    url = "http://api.bilibili.com/x/space/myinfo"
    cookie = extract_cookies(cookies)
    r = requests.get(url, cookies=cookie).text
    j = json.loads(r)
    uid = j['data']['mid']
    level = j['data']['level']
    current_exp = j['data']['level_exp']['current_exp']
    next_exp = j['data']['level_exp']['next_exp']
    sub_exp = int(next_exp) - int(current_exp)
    days = int(int(sub_exp) / 65)
    coin = getCoin()
    times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    msg = "【bili】" + str(times) + "\nWelcome! Current level is " + str(level) + "\nCurrent experience are " + str(
        current_exp) + "\nNot far from upgrading " + str(sub_exp) + "\nneed " + str(days) + " days\n" + \
          "Remaining silver coins are " + str(coin)
    print(msg)
    return msg


# 推荐动态
def getActiveInfo():
    url = "http://api.bilibili.com/x/web-interface/archive/related?aid=" + \
          str(7)
    cookie = extract_cookies(cookies)
    r = requests.get(url, cookies=cookie).text
    j = json.loads(r)
    return j


# 推荐动态第二种方式
def getVideo():
    random_page = random.randint(0, 20)
    url = "http://api.bilibili.cn/recommend?page=" + str(random_page)
    cookie = extract_cookies(cookies)
    r = requests.get(url, cookies=cookie).text
    j = json.loads(r)
    return j


# 投币 分享5次
def Task():
    coin_num = getCoin()
    # 需要投币的个数
    num = 5
    if coin_num <= num:
        num = coin_num
    coin_count = 0
    count = 0
    while True:
        j = getVideo()
        list_len = len(j['list'])
        random_list = random.randint(1, list_len - 1)
        bvid = j['list'][random_list]['bvid']
        aid = j['list'][random_list]['aid']
        print(str(count) + ' ---- ' + str(bvid) + ' ---- ' + str(aid))
        count = count + 1
        toview(bvid)
        time.sleep(5)
        shareVideo(bvid)
        time.sleep(5)
        if coin_count < num:
            coin_code = tocoin(aid, bvid)
            if coin_code == -99:
                return
        if coin_code == 1:
            coin_count = coin_count + 1
        if coin_count == num:
            break
        print('----------------------')


# 观看视频【不会点赞投币】
def toview(bvid):
    playedTime = random.randint(10, 100)
    url = "https://api.bilibili.com/x/click-interface/web/heartbeat"
    data = {
        'bvid': bvid,
        'played_time': playedTime,
        'csrf': csrf
    }
    cookie = extract_cookies(cookies)
    try:
        r = requests.post(url, data=data, cookies=cookie).text
        j = json.loads(r)
        code = j['code']
        if code == 0:
            print('watching viedo successful!')
        else:
            print('watching viedo failed!')
    except:
        print('watching viedo failed!')


# 分享视频
def shareVideo(bvid):
    url = "https://api.bilibili.com/x/web-interface/share/add"
    data = {
        'bvid': bvid,
        'csrf': csrf
    }
    cookie = extract_cookies(cookies)
    # 需要请求头
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38",
    }
    try:
        r = requests.post(url, data=data, cookies=cookie, headers=header).text
        j = json.loads(r)
        code = j['code']
        if code == 0:
            print('share  successful!')
        else:
            print('share failed!')
    except:
        print('share failed!')


# 投币函数
def tocoin(aid, bvid):
    coinNum = getCoin()
    if coinNum == 0:
        print('not enough coin !')
        return -99
    url = "https://api.bilibili.com/x/web-interface/coin/add"
    headers = {
        'authority': 'api.bilibili.com',
        'method': 'POST',
        'path': '/x/web-interface/coin/add',
        'scheme': 'https',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.bilibili.com',
        'pragma': 'no-cache',
        'referer': 'https://www.bilibili.com/video/' + str(bvid) + '?spm_id_from=444.41.0.0',
        'sec-ch-ua': '"Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    data = {
        'aid': aid,
        'multiply': 1,
        'select_like': 1,
        'cross_domain': 'true',
        'csrf': csrf
    }
    cookie = extract_cookies(cookies)
    try:
        r = requests.post(url, data=data, headers=headers, cookies=cookie).text
        j = json.loads(r, strict=False)
        code = j['code']
        if code == 0:
            print(str(bvid) + ' toaddcoin successful !')
            return 1
        else:
            print(str(bvid) + ' toaddcoin failed!')
            return 0
    except:
        print(str(bvid) + ' toaddcoin failed!')
        return 0


# 一键三连
def toall(bvid):
    coinNum = getCoin()
    if coinNum == 0:
        print('not enough coin !')
        return -99
    url = "http://api.bilibili.com/x/web-interface/archive/like/triple"
    data = {
        'bvid': bvid,
        'csrf': csrf
    }
    cookie = extract_cookies(cookies)
    r = requests.post(url, data=data, cookies=cookie).text
    j = json.loads(r)
    code = j['code']
    if code == 0:
        print(str(bvid) + ' toaddcoin successful !')
        return 1
    else:
        print(str(bvid) + ' toaddcoin failed!')
        return 0


# 开启任务运行
def run():
    getInfo()
    Task()


# 云函数使用
def main_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    print("Received context: " + str(context))
    run()
    return ("------ end ------")


if __name__ == '__main__':
    run()