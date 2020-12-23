# -*- coding = utf-8 -*-
# @Time : 2020/9/1916:05
# @Author : lzl
# @File : spyder_bk.py
# @Software : PyCharm

import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import re
import xlwt
import sqlite3


def main():
    baseurl = "https://sh.fang.ke.com/loupan/pg"
    # askURL(baseurl)
    # 爬取网页
    datalist = getData(baseurl)
    # 保存数据到Excel
    # savepath = ".\\贝壳找房上海市房源数据.xls"
    # saveData(savepath, datalist)
    # 保存数据到SQLite
    dbpath = "room1000.db"
    saveData2DB(datalist, dbpath)


# 房源详情的规则
findLink = re.compile(r'<a.*href="(.*?)"')  # 获取房源的链接
findName = re.compile(r'<a.*href=".*?".*title="(.*?)"')    # 获取房源的名称
findStage = re.compile(r'<span class="resblock-type" style="background: .*;">(.*?)</span>')  # 获取房源是否在售这个状态
findType = re.compile(r'<span style="background: .*;">(.*?)</span>')   # 获取房源的类型
findPosition = re.compile(r'<i class="icon location-icon"></i>(.*?)</a>', re.S)     # 获取房源的位置
findAvePrice = re.compile(r'<span class="number">(.*?)</span>')    # 获取房源的平均价格
findSumPrice = re.compile(r'<div class="second">总价(.*?)</div>')  # 获取房源的总价
findArea = re.compile(r'<span class="area">建面 (.*?)</span>')   # 获取房源的建筑面积
findStyle = re.compile(r'<div class="resblock-tag">(.*?)</div>', re.S)   # 获取房源的特点


def getData(baseurl):   # 爬取网页
    datalist = []  # 储存爬取到的数据
    for i in range(0, 100):
        url = baseurl + str(i + 1)  # 测试爬取第一页网站的信息
        html = askURL(url)  # 得到第一页的html信息
        # 逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="resblock-desc-wrapper"):  # 查找符合要求的字符串，形成列表
            data = []  # 保存一个房源的所有信息
            item = str(item)  # 将item转化为字符串
            # print(item)
            # 房源的链接信息
            link = re.findall(findLink, item)[0]
            link = "https://sh.fang.ke.com/" + link
            data.append(link)
            # 房源的名称信息
            name = re.findall(findName, item)[0]
            data.append(name)
            # 房源的均价信息
            aveprice = re.findall(findAvePrice, item)[0]
            aveprice = aveprice
            data.append(aveprice)
            # 房源的总价信息
            sumprice = re.findall(findSumPrice, item)
            if len(sumprice) == 0:
                data.append(' ')  # 留空
            else:
                data.append(sumprice[0])
            # 房源的状态信息
            stage = re.findall(findStage, item)[0]
            data.append(stage)
            # 房源的类型信息
            typee = re.findall(findType, item)[0]
            data.append(typee)
            # 房源的位置信息
            position = re.findall(findPosition, item)[0]
            data.append(position.strip())
            # 房源的面积信息
            area = re.findall(findArea, item)
            if len(area) == 0:
                data.append(' ')  # 留空
            else:
                data.append(area[0])
            # 房源的描述信息
            style = re.findall(findStyle, item)[0]
            style = re.sub('\n<span>', '', style)  # 先把字符串消除
            style = re.sub('</span>', ' ', style)  # 中间加入空格
            style = re.sub('\n', '', style)
            data.append(style)

            datalist.append(data)
    return datalist


def askURL(url):    # 得到一个指定URL的内容
    head = {  # 模拟浏览器信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52"
    }  # 告诉豆瓣服务器我们是什么样的浏览器
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# def saveData(savepath, datalist):   # 保存数据到EXCEL
#     book = xlwt.Workbook(encoding='utf-8', style_compression=0)
#     sheet = book.add_sheet('上海市房源信息', cell_overwrite_ok=True)
#     col = ['房源链接', '房源名', '房源均价', '房源总价', '销售状态', '房源类型', '房源位置', '房源面积', '房源描述']
#     for i in range(0, len(col)):
#         sheet.write(0, i, col[i])
#     for i in range(0, 1000):
#         print("第%d条" % (i + 1))
#         data = datalist[i]
#         for j in range(0, 9):
#             sheet.write(i+1, j, data[j])    #数据
#     book.save(savepath)


def saveData2DB(datalist, dbpath):
    initdb(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            data[index] = '"' + data[index] + '"'
        sql = '''
                insert into room1000(
                    link, roomName, avePrice, sumPrice, roomState, roomType, roomPosition, area, description)
                    values(%s)
            ''' % ",".join(data)
        cur.execute(sql)
        conn.commit()
    conn.close()


def initdb(dbpath):
    sql = '''
            create table room1000
            (
                id integer primary key autoincrement,
                link text,
                roomName varchar,
                avePrice numeric,
                sumPrice varchar,
                roomState varchar,
                roomType varchar,
                roomPosition text,
                area varchar,
                description text
            )
            '''     # 创建数据表
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()