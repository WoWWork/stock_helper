import os
import csv

class file_manager:
	def __init__(self):
		self.csv_path = '..//data_sheet'
		self.txt_path = '..//msg_sheet' 
		if not os.path.exists(self.csv_path):
			try: os.makedirs(self.csv_path, exist_ok = True) 
			except OSError as error: print("Directory '%s' can not be created" % self.csv_path)
		if not os.path.exists(self.txt_path):
			try: os.makedirs(self.txt_path, exist_ok = True) 
			except OSError as error: print("Directory '%s' can not be created" % self.txt_path)
	
	def csv_read(self, name):
		rows = []
		try:
			with open(self.csv_path + '//' + name + '.csv', newline='') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
				for row in spamreader: rows.append(row)
				return rows
		except Exception as ex:
			print(ex.args)
			
	def csv_write(self, name, data):
		try:
			with open(self.csv_path + '//' + name + '.csv', 'a', newline='') as csvfile:
				spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|')
				spamwriter.writerow(data)
		except Exception as ex:
			print(ex.args)
			
	def txt_read(self, name):
		try:
			with open(self.txt_path + '//' + name + '.txt') as txtfile:
				print(txtfile.read())
				return txtfile.read()
		except Exception as ex:
			print(ex.args)

	def txt_write(self, name, data):
		try:
			with open(self.txt_path + '//' + name + '.txt', 'a', encoding='utf-8') as txtfile:
				txtfile.write(data + '\r\n')
		except Exception as ex:
			print(ex.args)

# maker = file_manager()			
# archive = input('Please enter the file name : ')

# maker.csv_write(archive, ['one', 'two', 'three', 'four', 'five'])
# datas = maker.csv_read('stockMenu')
# for row in datas: print(list(filter(None, row)))