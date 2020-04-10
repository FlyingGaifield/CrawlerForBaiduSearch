# CrawlerForBaiduSearch
Crawler For Baidu Search
爬虫百度搜索到的网站
这个小项目在老板的逼迫下做的
本想着网上随便扒一个，可发现好多程序只能访问第一页，不能访问后面的几页，所以就简单地再学习了一下，写了这个程序

## 功能
爬取百度搜索结果的标题和链接，每页十个
## 使用
python2 grab_baidu.py
还有个py文件是 url2io.py，是用来获取链接的正文，但是我使用下来抓取的文本内容并不是很稳定，所以还是注释(用##和一整段的注释)掉了
结果会存为一个excel文档 （标题，URL）格式

## 库 （pip）
beautifulsoup \
requests \
xlrd \
xlwt 
