import requests
import MySQLdb
from urllib.parse import urlencode
from multiprocessing.pool import Pool
from lxml import etree

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
}

print("please enter host(e.g localhost)\n")
host = input("your host:") or "localhost"
print("please enter user(e.g root)\n")
user = input("user name:") or "root"
print("please enter password(e.g 123456)\n")
password = input("password:") or "123456"
print("please enter database name(e.g DBName)\n")
dbname = input("database name:") or "exam"
print("please enter database charset(e.g utf8)\n")
charset = input("charset:") or "utf8"
db = MySQLdb.connect(host, user, password, dbname, charset=charset)
cursor = db.cursor()

def get_page(page):
    params = {
        'tpId': '80',
        'tqId': str(29678 + int(page)),
        'query': '',
        'asc': 'true',
        'order': '',
        'page': page  # 1 begin
    }
    base_url = 'https://www.nowcoder.com/ta/review-frontend/review?'
    url = base_url + urlencode(params)
    try:
        resp = requests.get(url, headers=headers)
        print (url)
        if resp.status_code == 200:
            selector = etree.HTML(resp.text)
            question = ''.join(selector.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]//text()'))
            answer = selector.xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[1]//text()')
            answer = "".join(answer)
            insertQuestion = "INSERT INTO `question`(`title`, `subtitle`, `description`, `create`, `last`) VALUES (%s, '', %s, '2021-03-01 09:23:21', '2021-03-01 09:23:24')"
            out = "INSERT INTO `exam`.`question`(`title`, `subtitle`, `description`, `create`, `last`) VALUES ({}, '', {}, '2021-03-01 09:23:21', '2021-03-01 09:23:24')"
            #print(out.format(question,answer))
            param = (question,question)
            cursor.execute(insertQuestion,param)
            qid = cursor.lastrowid
            insertAnswer = "INSERT INTO `answer`(`ans`, `description`) VALUES (%s, %s)"
            param = (answer,'')
            cursor.execute(insertAnswer,param)
            aid = cursor.lastrowid
            insertQA = "INSERT INTO `exam`.`question_answer`(`qid`, `tid`) VALUES (%s, %s)"
            param = (str(qid),str(aid))
            cursor.execute(insertQA,param)
            insertQM = "INSERT INTO `exam`.`question_maker`(`qid`, `uid`) VALUES (%s, 1)"
            param = (str(qid),)
            cursor.execute(insertQM,param)
            insertQTopic = "INSERT INTO `exam`.`question_topic`(`qid`, `tid`) VALUES (%s, 2)"
            cursor.execute(insertQTopic,param)
            insertQType = "INSERT INTO `exam`.`question_type`(`qid`, `tid`) VALUES (%s, 1)"
            cursor.execute(insertQType,param)
            db.commit()
    except Exception as e:
        print (e)


def main(page):
    get_page(page)


if __name__ == '__main__':
    # pool = Pool()
    # pool.map(main, [i for i in range(1,501)])
    # pool.close()
    # pool.join()
     for i in range(1,502): main(i)

cursor.close()
db.close()
print("completed")
