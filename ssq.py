import requests
import pymysql
from bs4 import BeautifulSoup

download_url = 'http://caipiao.163.com/award/ssq/2018{}.html'

def download_page(url):
    """获取url地址页面内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
    }
    data = requests.get(url, headers=headers).content
    return data

def get_conn():
    """建立数据库连接"""
    conn = pymysql.connect(host='localhost',
                                user='root',
                                password='root',
                                db='python',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    return conn

def insert(conn, info):
    """数据写入数据库"""
    with conn.cursor() as cursor:
        sql = "INSERT INTO `t_carnumber` (`cars`, `fulltime`, `termnumber`, `specialcars`, `lottery_code`) VALUES (" \
              "%s, %s, %s, %s, %s) "
        cursor.execute(sql, info)
        conn.commit()


def get_li(doc):
    soup = BeautifulSoup(doc, 'html.parser')
    content = soup.find('div', class_='search_zj_left')
    cars = []

    fulltime = content.find('span', attrs={'id': 'time'}).get_text()
    for c in content.find('p', attrs={'id' : 'zj_area'}).find_all('span'):
        cars.append(c.string)
    specialcars = cars.pop(len(cars)-1)
    termnumber = soup.find(name='a', attrs={'id': 'change_date'}).get_text()
    conn = get_conn()  # 建立数据库连接  不存数据库 注释此行
    lottery_code = '5000'
    strs = ","
    info = [strs.join(cars), fulltime, termnumber, specialcars, lottery_code]
    insert(conn, tuple(info))
    print(str(info))
    conn.close()


def main():
    for i in range(80, 113):
        pageSize = str(i).rjust(3, "0")
        print(pageSize)
        url = 'http://caipiao.163.com/award/ssq/2018{}.html'.format(pageSize)
        doc = download_page(url)
        get_li(doc)


if __name__ == '__main__':
    main()
