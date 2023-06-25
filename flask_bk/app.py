from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


# 模板文件
@app.route('/temp')     # 路由解析
def temp():
    return render_template('temp.html')     # 主页


@app.route('/')     # 路由解析
def index():
    return render_template('home.html')     # 主页


@app.route('/home')
def home():
    return render_template('home.html')     # 主页


@app.route('/info')
def info():
    datalist = []
    conn = sqlite3.connect("room.db")
    cur = conn.cursor()
    sql = "select * from room"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    conn.close()
    return render_template('info.html', rooms=datalist)     # 信息页


@app.route('/price')
def price():
    num = []
    con = sqlite3.connect('room.db')
    cur = con.cursor()
    sql1 = '''
             select sum(case when avePrice between 1 and 9999 then 1 else 0 end) as A,
                    sum(case when avePrice between 10000 and 19999 then 1 else 0 end) as B,
                    sum(case when avePrice between 20000 and 29999 then 1 else 0 end) as C,
                    sum(case when avePrice between 30000 and 39999 then 1 else 0 end) as D,
                    sum(case when avePrice between 40000 and 49999 then 1 else 0 end) as E,
                    sum(case when avePrice between 50000 and 50000000 then 1 else 0 end) as F
                    from room 
                '''
    data1 = cur.execute(sql1)
    for item in data1:
        for i in range(0,6):
            num.append(item[i])
    sql2 = "select AVG(avePrice) from room where avePrice between 1 and 50000000"
    data2 = cur.execute(sql2)
    for item in data2:
        ave = int(item[0])
    cur.close()
    con.close()

    return render_template('price.html', num=num, ave=ave)     # 价格页


@app.route('/area')
def area():
    return render_template('area.html')     # 区域页


@app.route('/word')
def word():
    return render_template('word.html')     # 词云页


if __name__ == '__main__':
    app.run()
