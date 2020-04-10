# -*- coding:utf-8 -*-
import os
import requests
import time
#import csv
####import re
from bs4 import BeautifulSoup
import urllib2
####from jparser import PageModel
####import url2io
import xlrd
import xlwt

# 设置默认encoding方式
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

####token = 'xxxx' #之前我自己的token不再公开，请到url2io官网注册获取token
####api = url2io.API(token)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}


    
def main(): 
	query = 'xxxx'
	#初始网页，我发现修改ＰＮ＝　０，１０，２０不管用，所以试图在每一页寻找下一页的ｕｒｌ
	url = 'http://www.baidu.com/s?wd=%s&pn=%i' % (query,0)
	url_list = ['网址']
	title_list =['题目']
	for k in range(0,20):
			#待抓取的网页地址
			
			print(url)
			print('---------page ' ,k,'------------')
			content = requests.get( url,headers=headers, verify=False, timeout=10)
			#使用BeautifulSoup解析html
			#print(content.text)
			soup = BeautifulSoup(content.text,'html.parser')
			# 找到左侧文本 一般有一个
			whole_search = soup.select('div[id="content_left"]')
			
			for x in whole_search:
				#找到搜索文本，一般有十个
				#test = x.find_all(name = "div", attrs = { "class": re.compile( "result")})
				test = x.find_all(name = "div", attrs = {"class": "c-tools"})
				#print(len(test))
				print(len(test))
				content_detail = ''
				for y in test :
					#得到了每个搜索记录的网址
					#print(y)
					#each_url = y.get('mu')
					#print('current url is :', y.get('data-tools'))
					title_and_url =  y.get('data-tools').split('","')
					title_sole = title_and_url[0][10:]
					url_sole = title_and_url[1][6:-2]

					print(title_sole)
					print(url_sole)	
					url_list.append(str(url_sole))
					title_list.append(str(title_sole))
					#each_content = requests.get(each_url,headers = headers, verify =False, timeout=10)
					#print(BeautifulSoup(each_content.text,'html.parser'))
					#获取每个url的文本信息
					#####################################################################################
					'''
					try:
						print('check1')
						time.sleep(5)
						ret = api.article(url=each_url, fields=['text', 'next'])
						content_detail = ret['text'].replace('\r','').replace('\n','')
						print(content_detail)
						#content.append(ret['text'].replace('\r','').replace('\n',''))

					except:
						try:
							print('check2')
							time.sleep(5)
							ret = api.article(url=each_url, fields=['text'])
							content_detail = ret['text'].replace('\r','').replace('\n','')
							#content.append(ret['text'].replace('\r','').replace('\n',''))
						except:
							try:
								try:
									print('check3')
									time.sleep(5)
									html = requests.get(each_url,headers=head, timeout = 10 ).text.decode('utf-8')
								except:
									print('check４')
									time.sleep(5)
									html = requests.get(each_url,headers=headers,timeout = 10 ).text.decode('gbk')
								pm = PageModel(html)
								result = pm.extract()
								ans = [ x['data'] for x in result['content'] if x['type'] == 'text']
								content_detail = ''.join(ans)
								#content.append(''.join(ans))
							except Exception as e:
								print('check51')
								print(e)
								print(each_url)
								content = '' 
								#content.append('')
								pass

					print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')
					break
					'''
					####################################################################################################
					print('------------------------------------')

				#找到下一页
			try:
				next_page = soup.find('div', id='page') 
				#print(test)
				index =0 
				for x in next_page :
					#print(x)
					#print('---------------------')
					if index == len(next_page)-2:
						#print(x.get('href'))
						url = 'http://www.baidu.com'+x.get('href')
					index +=1 
			except:
				break

			#allNews = soup.find_all('div', { 'id', 'result c-container '})
			#allNews = soup.select("div.result.c-container")
			#for hotNews in allNews:
				#h3 = hotNews.find(name = "h3", attrs = { "class": re.compile( "t")}).find('a')
				#title.append(h3.text.replace("\"",""))
				#div = hotNews.find(name = "div", attrs = { "class": re.compile( "c-abstract")})
				#abstract.append(div.text.replace("\"",""))
				#a = hotNews.find(name = "a", attrs = { "class": re.compile( "c-showurl")})
				#detail_url = a.get('href')
				#link.append(detail_url)
	#写入excel
	workbook = xlwt.Workbook(encoding = 'utf-8')  # 新建一个工作簿
	sheet = workbook.add_sheet('sheet1')  # 在工作簿中新建一个表格
	for i in range(0, len(title_list)):
		sheet.write(i, 0, title_list[i]) 
		sheet.write(i, 1, url_list[i])  # 像表格中写入数据（对应的行和列）
	workbook.save('result.xls')  # 保存工作簿
	print("xls格式表格写入数据成功！")



if __name__ == '__main__':
	print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
	print('starting...')

	main()

	print('finished')
	print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
