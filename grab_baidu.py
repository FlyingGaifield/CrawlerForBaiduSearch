# -*- coding:utf-8 -*-
# Copyright @ Gaifield Song
# 2020/04/13
import os
import requests
import time
import re
from bs4 import BeautifulSoup
import urllib2

import xlrd
import xlwt
from xlutils.copy import copy
from collections import defaultdict, OrderedDict
from goose import Goose
from goose.text import StopWordsChinese
import eventlet # 防止读取正文的时候超时
# 设置默认encoding方式
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


g = Goose({'stopwords_class': StopWordsChinese})
eventlet.monkey_patch()

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}




# 读取ｅｘｃｅｌ文本
# 格式　：
# 姓名（搜索的人物）　　　主类（主要关键词）　次类（次要关键词）　剔除类（剔除包换此项的链接）
def read_from_excel(input_excel):
	# input_excel : '文件名'
	output = []
	workbook = xlrd.open_workbook(input_excel)  # 打开工作簿
	sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
	worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
	nrows = worksheet.nrows  # 获取表格中已存在的数据的行数
	for i in range(1, nrows):
		temp = [worksheet.row_values(i)[0].decode('utf-8'), worksheet.row_values(i)[1].decode('utf-8'), worksheet.row_values(i)[2].decode('utf-8'), worksheet.row_values(i)[3].decode('utf-8')]
		output.append(temp)
	return output
	# [[姓名１，　主类１，　次类１，　剔除类１]，　[姓名2，　主类2，　次类2，　剔除类2], ..........]




def write_to_excel(search_item, result_dict, output_excel, index):


	#统计各类条目数的数量　【不包含关键词，　包含关键词，不确定】
	ans = [0,0,0]
	for x in result_dict.items():
		ans[int(x[1][2])]+=1





	if  index==1 :
		# 处理sheet1, 每一行包含　姓名　条目数
		workbook = xlwt.Workbook(encoding = 'utf-8')  # 新建一个工作簿
		sheet = workbook.add_sheet('总页')  # 在工作簿中新建一个表格
		sheet.write(0, 0, "姓名")
		sheet.write(0, 1, "总条目数")
		sheet.write(0, 2, "包含主类关键词条目数")
		sheet.write(0, 3, "不包含主类关键词条目数")
		sheet.write(0, 4, "不确定条目数")
		sheet.write(index, 0, search_item[0].decode('utf-8')) 
		sheet.write(index, 1, len(result_dict))  # 像表格中写入数据（对应的行和列）
		sheet.write(index, 2, ans[0])  # 像表格中写入数据（对应的行和列）
		sheet.write(index, 3, ans[1])  # 像表格中写入数据（对应的行和列）
		sheet.write(index, 4, ans[2])  # 像表格中写入数据（对应的行和列）
		# 处理详情页
		sheet_detail = workbook.add_sheet(search_item[0].decode('utf-8'))
		sheet_detail.write(0, 0, "关键词".decode('utf-8'))
		sheet_detail.write(0, 1, "主类".decode('utf-8'))
		sheet_detail.write(0, 2, "是否包含主类（１：包含　０：不包含　２：不确定）".decode('utf-8'))
		sheet_detail.write(0, 3, "题目".decode('utf-8'))
		sheet_detail.write(0, 4, "网站".decode('utf-8'))
		sheet_detail.write(0, 5, "详细内容".decode('utf-8'))
		for i , item in enumerate(result_dict.items()):
			sheet_detail.write(i+1, 0, item[1][0]) 
			sheet_detail.write(i+1, 1, item[1][1]) 
			sheet_detail.write(i+1, 2, item[1][2])   
			sheet_detail.write(i+1, 3, item[0]) 
			sheet_detail.write(i+1, 4, item[1][3])  
			sheet_detail.write(i+1, 5, item[1][4]) 
		workbook.save(output_excel) 

	else:
		workbook =  xlrd.open_workbook(output_excel)
		sheets = workbook.sheet_names() 
		sheet = workbook.sheet_by_name(sheets[0])
		rows_old = sheet.nrows
		new_workbook = copy(workbook) 
		new_sheet = new_workbook.get_sheet(0)
		new_sheet.write(index, 0 , search_item[0].decode('utf-8')) 
		new_sheet.write(index, 1 , len(result_dict))  # 像表格中写入数据（对应的行和列）	
		new_sheet.write(index, 2, ans[0])  # 像表格中写入数据（对应的行和列）
		new_sheet.write(index, 3, ans[1])  # 像表格中写入数据（对应的行和列）
		new_sheet.write(index, 4, ans[2])  # 像表格中写入数据（对应的行和列）	
		
		# 处理详情页
		sheet_detail = new_workbook.add_sheet(search_item[0].decode('utf-8'))
		sheet_detail.write(0, 0, "关键词".decode('utf-8'))
		sheet_detail.write(0, 1, "主类".decode('utf-8'))
		sheet_detail.write(0, 2, "是否包含主类（１：包含　０：不包含　２：不确定）".decode('utf-8'))
		sheet_detail.write(0, 3, "题目".decode('utf-8'))
		sheet_detail.write(0, 4, "网站".decode('utf-8'))
		sheet_detail.write(0, 5, "详细内容".decode('utf-8'))
		for i , item in enumerate(result_dict.items()):
			sheet_detail.write(i+1, 0, item[1][0]) 
			sheet_detail.write(i+1, 1, item[1][1]) 
			sheet_detail.write(i+1, 2, item[1][2])   
			sheet_detail.write(i+1, 3, item[0]) 
			sheet_detail.write(i+1, 4, item[1][3])  
			sheet_detail.write(i+1, 5, item[1][4]) 
		new_workbook.save(output_excel)  # 保存工作簿

	print("xls格式表格写入数据成功！")





    
def main(search_item): 
	# search_whole : [[姓名１，　主类１，　次类１，　剔除类１]，　[姓名2，　主类2，　次类2，　剔除类2], ..........]
	result_dict = OrderedDict()
	for main_cat  in search_item[1].split('　'):#注意这里是中文的空格
		for query in search_item[2].split('　'):#注意这里是中文的空格
			query = search_item[0].decode('utf-8')+' '+main_cat.decode('utf-8')+' '+ query.decode('utf-8')
			#初始网页，我发现修改ＰＮ＝　０，１０，２０不管用，所以试图在每一页寻找下一页的ｕｒｌ
			url = 'http://www.baidu.com/s?wd=%s&pn=%i' % (query,0)
			for k in range(0, 20):
					#待抓取的网页地				
					print(url)
					print('---------page ' ,k,'------------')
					content = requests.get( url,headers=headers,  verify =False, timeout=10 )
					#使用BeautifulSoup解析html
					#print(content.text)
					soup = BeautifulSoup(content.text,'html.parser')
					#print(content.text)
					# 找到左侧文本 一般有一个
					whole_search = soup.select('div[id="content_left"]')
					#print(whole_search)
					for x in whole_search:
						#找到搜索文本，一般有十个
						#test = x.find_all(name = "div", attrs = { "class": re.compile( "result")})
						test = x.find_all(name = "div", attrs = {"class": "c-tools"})
						#print(len(test))
						print(len(test))

						for y in test :
							content_detail = ''
							#得到了每个搜索记录的网址
							#each_url = y.get('mu')
							#print('current url is :', y.get('data-tools'))
							title_and_url =  y.get('data-tools').split('","')
							title_sole = title_and_url[0][10:]
							url_sole = title_and_url[1][6:-2]

							with eventlet.Timeout(4,False):
								# 这里是用ｇｏｏｓｅ来提取
								try:							
									article = g.extract(url=url_sole)
									content_detail = article.cleaned_text
								except:
									content_detail = ''		

							#if True:
							# 如果剔除类的词语都不要获取的文本中则是我们需要的信息 
							remove_list = search_item[3].split('　')
							if title_sole  not in result_dict  :
								flag= 1
								for each_remove in remove_list:
									if each_remove.decode('utf-8') in content_detail:
										flag = 0 
										break
								if flag == 1 :	
									if content_detail == '':
										print(title_sole)
										print(url_sole)	
										result_dict[title_sole] = [query.decode('utf-8'), main_cat.decode('utf-8'), 2, url_sole, content_detail]	
									else:										
										if main_cat.decode('utf-8') in content_detail:							
											print(title_sole)
											print(url_sole)	
											result_dict[title_sole] = [query.decode('utf-8'), main_cat.decode('utf-8'), 1,url_sole, content_detail]	
										else:
											result_dict[title_sole] = [query.decode('utf-8'), main_cat.decode('utf-8'), 0,url_sole, content_detail]						
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
					time.sleep(1)
	#return value [搜索的关键词　，主类关键词，　正文是否包含主类关键词，　网址，　正文内容]
	return result_dict


		
		

			



if __name__ == '__main__':
	print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
	print('starting...')
	print('######################################################################')

	input_xls = raw_input("请输入excel文件名（例如input1.xls）：:")
	output_xls = input_xls.split('.')[0]+'_output.xls'
	#main()
	search_whole = read_from_excel(input_xls)
	for i, search_item in enumerate(search_whole):
		result_dict = main(search_item)
		write_to_excel(search_item, result_dict, output_xls, i+1)

	print('finished')
	print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
