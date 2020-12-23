# -*- coding = utf-8 -*-
# @Time : 2020/9/2415:46
# @Author : lzl
# @File : wordCloud.py
# @Software : PyCharm

import jieba    # 分词
from matplotlib import pyplot as plt
from wordcloud import WordCloud     # 词云
from PIL import Image   # 图片处理
import numpy as np
import sqlite3


# 提取词云所需要的字（词）
con = sqlite3.connect("room.db")
cur = con.cursor()
sql = "select description from room"
data = cur.execute(sql)
text = ''
for item in data:
    text = text + item[0]
cur.close()
con.close()


# 分词
cut = jieba.cut(text)
string = ' '.join(cut)


# 设置遮罩图片
img = Image.open("tree.jpg")
img_array = np.array(img)
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path=r'C:\Windows\Fonts\msyh.ttc'
)
wc.generate_from_text(string)


# 绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')


# 输出词云图片到文件
plt.savefig(r'.\word.jpg', dpi=800)
