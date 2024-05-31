import time
import requests
from selenium import webdriver
import pandas as pd
import datetime as dt
import yfinance as yf
import bs4
import re
from enum import Enum
import file_module as fm

# stock_id = input('Please enter stock code : ')
# date = (dt.date.today()-dt.timedelta(days=1)).strftime("%Y%m%d")

def twse_stock(date, stock_no):
	payload = {'date':date, 'stockNo':stock_no}
	stock_data = requests.get('https://www.twse.com.tw/rwd/zh/\
			afterTrading/STOCK_DAY', params=payload)
	json_data = stock_data.json()
	# print(stock_data.url)
	# print(json_data)
	return json_data

def twse_eps(date, stock_no, format='json'):
	url = f'https://www.twse.com.tw/rwd/zh/afterTrading/BWIBBU?date={date}&stockNo={stock_no}&response={format}'
	response = requests.get(url)
	json_data = response.json()
	print(response.url)
	print(json_data)
	return json_data

def yahoo_stock(stock_no):
	url = 'https://tw.stock.yahoo.com/quote/' + stock_no + '.TW'
	response = requests.get(url)
	fields=[]
	datas=[]
	if response.status_code == requests.codes.ok:
		html = response.content
		soup = bs4.BeautifulSoup(html, 'html.parser')
		time_element = soup.find('section', {'id':'qsp-overview-realtime-info'}).find('time')
		table_soups = soup.find('section',\
						{'id':'qsp-overview-realtime-info'}).find('ul').find_all('li')	
		for table_soup in table_soups:
			table_datas = table_soup.find_all('span')
			for num, table_data in enumerate(table_datas):
				if table_data.text == '': continue
				if num == 0: fields.append(table_data.text)
				else: datas.append(table_data.text)
	df = pd.DataFrame([datas], columns=fields)
	df.insert(0, '日期', time_element['datatime'])
	df.insert(1, '股號', stock_no)	
	print(df)
	return df

def yahoo_finance(stock_id, market='.TW', end=dt.date.today(), days_long=5):
	stock = stock_id + market
	start = end - dt.timedelta(days=days_long)
	stock_data = yf.download(stock, start=start, end=end)
	print(stock_data.tail())
	return stock_data.tail()

class mega_category(Enum):
	headline = '1'
	internation = '2'
	forexbond = '4'
	domestic = '5'
	rawMaterial = '6'
def mega_news(type, date, page='1', retry=0):
	url = f'https://fund.megabank.com.tw/ETFWeb/HTML/ETNEWS.DJHTM#TYPE={type}&DATE={date}&PAGE={page}'
	Firefox_options = webdriver.FirefoxOptions()
	Firefox_options.add_argument('--headless')
	Firefox_options.add_argument('--no-sandbox')
	Firefox_options.add_argument('--disable-gpu')
	driver = webdriver.Firefox(options=Firefox_options)
	driver.get(url)
	time.sleep(1)
	elements = driver.find_elements("xpath", '//*[@id="showtemplate1"]/table/tbody/tr')
	if len(elements) == 0 and retry < 2: mega_news(type, date, page, retry+1)
	daytimes = []
	titles = []
	links = []
	match = re.compile(r".*\('(.*)'\)")
	idx = 0
	for element in elements:
		if idx > 0:
			daytimes.append(element.find_elements("xpath", '//td')[2 * idx].text)
			titles.append(element.find_elements("xpath", '//td')[2 * idx + 1].text)
			links.append(re.search(match, element.find_elements("xpath", '//td/a')[idx - 1].get_attribute("href")).group(1))
		idx = idx + 1
	io_f = fm.file_manager()
	for idx, link in enumerate(links):
		url = f'https://fund.megabank.com.tw/ETFData/djhtm/ETNEWSContentMega.djhtm?TYPE={type}&DATE={date}&PAGE={page}&A={link}'
		driver.get(url)
		node_doc = driver.find_elements("xpath", '//*[@id="content"]/table/tbody/tr')[1]
		io_f.txt_write(mega_category(type).name + '_' +  daytimes[idx] + '_' + str(idx), links[idx] + '\r\n')
		io_f.txt_write(mega_category(type).name + '_' +  daytimes[idx] + '_' + str(idx), titles[idx] + '\r\n')
		io_f.txt_write(mega_category(type).name + '_' +  daytimes[idx] + '_' + str(idx), node_doc.text + '\r\n')
	driver.quit()
	# print(daytimes)
	# print(titles)
	# print(links)

def yahoo_news(aspect, end=dt.datetime.now().strftime("%Y-%m-%dM:%S")):
	print(end)
	url = 'https://tw.news.yahoo.com' + aspect
	print(url)
	siteMark = requests.get(url)
	if siteMark.status_code == requests.codes.ok:
		soup = bs4.BeautifulSoup(siteMark.text, 'html.parser')
		links = []
		titles = []
		match = re.compile(r'<.*>')
		for item in soup.find('div', {'id':'Main'}).find_all('a'):
			print(item['href'])
			phrase = match.sub('', item.decode_contents())
			print(phrase)
			links.append(item['href'])
			titles.append(phrase)
			
class udn_category(Enum):
	main = '0'
	noneSort = '99'
	important = '1'
	entertainment = '8'
	society = '2'
	local = '3'
	internation = '5'
	china = '4'
	financial = '6'
	stock = '11'
	sport = '7'
	living = '9'
	tech = '13'
	education = '12'
def udn_news(category):
	url = f'https://udn.com/news/breaknews/1/{category}#breaknews'
	Firefox_options = webdriver.FirefoxOptions()
	Firefox_options.add_argument('--headless')
	Firefox_options.add_argument('--no-sandbox')
	Firefox_options.add_argument('--disable-gpu')
	driver = webdriver.Firefox(options=Firefox_options)
	driver.get(url)
	last_height = driver.execute_script("return document.body.scrollHeight")
	links = []
	titles = []
	daytime = []
	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(1)
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height: break
		last_height = new_height
	elements = driver.find_elements("xpath", '//*[@id="breaknews"]//*/div[@class="story-list__text"]')
	idx = 0
	for element in elements:
		links.append(element.find_elements("xpath", '//h2/a')[idx].get_attribute("href"))
		titles.append(element.find_elements("xpath", '//h2/a')[idx].get_attribute("title"))
		daytime.append(element.find_elements("xpath", '//div/time')[idx].text)
		# print(element.find_elements("xpath", '//h2/a')[idx].get_attribute("href"))
		# print(element.find_elements("xpath", '//h2/a')[idx].get_attribute("title"))
		# print(element.find_elements("xpath", '//div/time')[idx].text)
		idx = idx + 1
	driver.quit()
	io_f = fm.file_manager()
	for idx, link in enumerate(links):
		siteMark = requests.get(link)
		content = ''
		if siteMark.status_code == requests.codes.ok:
			soup = bs4.BeautifulSoup(siteMark.text, 'html.parser')
			print(soup)
			for item in soup.find('section', {'class':'article-content__editor'}).find_all('p'):
				content = content + item.text
			io_f.txt_write(udn_category(category).name + '_' + daytime[idx] + '_' + str(idx), links[idx] + '\r\n')
			io_f.txt_write(udn_category(category).name + '_' + daytime[idx] + '_' + str(idx), titles[idx] + '\r\n')
			io_f.txt_write(udn_category(category).name + '_' + daytime[idx] + '_' + str(idx), content + '\r\n')
			# print(content)

# yahoo_news('/stock')
# twse_stock('20240510', stock_id)		
# yahoo_stock(stock_id)
# yahoo_finance(stock_id)
# mega_news('1', '2023/12/14')
# udn_news('11')