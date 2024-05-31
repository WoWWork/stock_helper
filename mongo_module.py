import numpy as np
import pymongo
import datetime as dt
import pandas as pd
import time
import file_module
import crawl

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
dblist = myclient.list_database_names()

def check_exist(dbname, collection):
    if dbname in dblist:
        mydb = myclient[dbname] 
        collist = mydb.list_collection_names()
        if collection in collist: return mydb[collection]
    return None

def import_stock_id(dbname, collection, datas):
    mycol = check_exist(dbname, collection)
    industry = ''
    ListOrOTC = ''
    if mycol != None:
        for idx in range(0, len(datas[0]), 2):
            if len(datas[0]) % 2 != 0: continue
            for idy in range(len(datas)):
                try:
                    int(datas[idy][idx])
                    item = {"stock_id": datas[idy][idx], "name": datas[idy][idx+1], "industry":industry, "listOrOTC":ListOrOTC}
                    x = mycol.insert_one(item)
                except ValueError as ex:
                    ListOrOTC = datas[idy][idx]
                    industry = datas[idy][idx+1]
                except IndexError: break

def import_stock_prices(dbname, collection, stock_id, days_long):
    datas = crawl.yahoo_finance(stock_id, days_long=days_long)
    date = str(datas['Open']).split()[1]
    open = str(datas['Open']).split()[2]
    high = str(datas['High']).split()[2]
    low = str(datas['Low']).split()[2]
    close = str(datas['Close']).split()[2]
    volume = str(datas['Volume']).split()[2]
    item = {"Date":date, "Open":open, "High":high, "Low":low, "Close":close, "Volume":volume}
    datas_update(dbname, collection, {"stock_id":str(stock_id)}, item)

def import_twse_prices(dbname, collection, date, stock_id):
    datas = crawl.twse_stock(date, stock_id)
    print(datas['fields'])
    print(datas['data'][len(datas['data']) - 1])
    item = {"Date":datas['data'][len(datas['data']) - 1][0], 
            "Open":datas['data'][len(datas['data']) - 1][3],
            "High":datas['data'][len(datas['data']) - 1][4],
            "Low":datas['data'][len(datas['data']) - 1][5],
            "Close":datas['data'][len(datas['data']) - 1][6],
            "Volume":datas['data'][len(datas['data']) - 1][1]}
    datas_update(dbname, collection, {"stock_id":str(stock_id)}, item)

def datas_query(dbname, collection, condition, display):
    mycol = check_exist(dbname, collection)
    if mycol != None:
        mydoc = mycol.find(condition, display)
        return mydoc

def datas_update(dbname, collection, query, values):
    mycol = check_exist(dbname, collection)
    if mycol != None:
        pharse = {"$set":  values }
        mycol.update_one(query, pharse)

def datas_clear(dbname, collection):
    mycol = check_exist(dbname, collection)
    if mycol != None: x = mycol.delete_many({})

# maker = file_module.file_manager()
# datas = maker.csv_read('stockMenu')
# rows = []
# for row in datas: rows.append(list(filter(None, row)))
# import_stock_id('admin', 'stock', rows)

# items = datas_query('admin', 'stock', '', {"stock_id": 1, "_id": 0})
# for item in list(items):
#     try:
#         # print(item)
#         time.sleep(1)
# import_twse_prices('admin', 'stock', dt.date.today().strftime("%Y%m%d"), '5426')
#     except Exception as ex:
#         print(ex)
#         continue

items = datas_query('admin', 'stock', '', {"stock_id": 1, "_id": 0})
for item in list(items):
    import_stock_prices('admin', 'stock', item['stock_id'], 1)