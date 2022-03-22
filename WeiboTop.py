import requests
from bs4 import BeautifulSoup
import sqlite3
import time


def create_database_table(database, table_name):
    database_connect = sqlite3.connect(database)
    print("open database:%s successfully" % database)
    database_cur = database_connect.cursor()
    # Create table
    try:
        database_cur.execute("create table %s \
         (num INTEGER PRIMARY KEY, top_content TEXT, \
         heat_index INTEGER, type TEXT, timer TEXT);" % table_name)
    except:
        print("table:%s has existed" % table_name)
    return database_cur, database_connect


def insert_database_table(database_cur, database_connect, table_name, values):
    database_cur.execute("INSERT INTO %s VALUES(?,?,?,?,?);" %
                         table_name, (None,  values[0], values[1], values[2], values[3]))
    database_connect.commit()


if __name__ == '__main__':
    while True:
        # 连接数据库
        cursor, conn = create_database_table("customers.db", 'WeiboTop')

        print('Start Tasks at {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))

        # 爬取数据
        url = "https://s.weibo.com/top/summary/"
        payload = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'Cookie': 'SCF=AiWdpaH_Y7pzXIvFFmZtBd_IxyxJvUjE4bmT1ncQgfawXC3egVEHVYVCWZn1gof32ouCwDtGYVyzYe4Ucb9sxJg.; SUB=_2AkMVbn0MdcPxrAVRkfsczmPiZI5H-jymuxT6An7uJhMyAxgP7gcrqSVutBF-XEsPiKaQeLlNuvqGnu4pHPhuPxQr; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9W59l_aEpkCML9k_QihPWdSw5JpV2PUydJUA9gyfqgREeh2NTbQ3; _s_tentry=link.zhihu.com; Apache=9500400252260.26.1647506023328; SINAGLOBAL=9500400252260.26.1647506023328; UOR=link.zhihu.com,s.weibo.com,link.zhihu.com; ULV=1647506023512:1:1:1:9500400252260.26.1647506023328:'
        }
        response = ''

        try:
            response = requests.request("GET", url, headers=headers, data=payload)
        except requests.HTTPError as e:
            print(e)

        if response:
            now_time = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())
            soup = BeautifulSoup(response.text, 'lxml')
            target = soup.find('tbody').find_all('tr')
            for tr in target:
                data = tr.text.split('\n')
                values = (data[1], data[3], data[5], now_time)
                print(values)
                insert_database_table(cursor, conn, 'WeiboTop', values)

        # print(cursor.execute("select * from WeiboTop").fetchall())
        conn.close()

        time.sleep(600)
