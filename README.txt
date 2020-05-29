
Copyright @ Gaifield Song
2020/04/13

1. 说明

此程序是爬虫百度搜索并且进行自动筛选关键词
1.1 输入为excel表格，每一行为姓名＋主类关键词（必须包含）＋次类关键词＋剔除类关键词，每一个格子内的关键词需要用中文输入法的空格相隔
1.2 输出:

第一页记录每个　搜索姓名　的条目数　（包含主关键词的条目数，　不包含主关键词的条目数，　不确定的链接数量）
之后的每一页包含一个姓名的详细信息：关键词＋主类搜索词＋是否包含主类关键词（０：不包括，１：包括，２：不确定）＋标题＋链接＋详细内容



2. 安装
python2 
pip2 install requests  
pip2 install beautifulsoup4
pip2 install urllib2
pip2 install xlrd
pip2 install xlwt
pip2 install xlutils
pip2 install eventlet
goose安装
git clone https://github.com/grangier/python-goose.git
cd python-goose
pip install -r requirements.txt
python setup.py install



3. 使用
python2 grab_baidu.py
会提示你输入, 输出为同名加上 _output后缀
