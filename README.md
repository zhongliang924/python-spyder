# python-spyder
python爬虫实战

以贝壳找房网站作为实例，“https://sh.fang.ke.com/loupan/pg1”
提取上海市一千套房源的数据，数据存放在excel表中，也可以在room.db数据库中查看。
该实例通过worldCloud.py生成词云，把关键词绘制成词云树。

使用python的flask框架，进行数据可视化，引入爬虫爬取的room.db数据库作为数据支撑，得到主页，信息页、价格页、区域页和词云页共五个页面，并编写相应的HTML文件展示我们需要的内容，这些HTML文件存在templates文件夹中。
