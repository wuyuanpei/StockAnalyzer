import requests
import os

# Stock data from online API
# year:         数据年份
# stocks_file:  股票代码文件,每一行的格式为 XYYYYYY/ZZ..Z\n
#               X 为0/1 上或深
#               Y 为6位股票代码
#               Z 为股票名称(不限字数)
# write_folder: 写入文件夹
def store_data(year="2020", stocks_file="stock_test.txt", write_folder="./data"):
    # fileList = os.listdir(write_folder)
    with open(stocks_file) as f:
        for line in f:
            # if line[0:7]+"_"+year+".json" in fileList: # 如果文件已经存在
            #     print("Already Stored:"+line[8:-1]+"/"+year)
            #     continue
            url = "http://img1.money.126.net/data/hs/kline/day/history/"+year+"/"+line[0:7]+".json"
            while True:
                try:
                    r = requests.get(url)
                except BaseException: # 请求失败,可能是因为被暂时屏蔽
                    print("Cannot connect to server!")
                else:
                    break
                
            if r.status_code == 404: # 请求的股票不存在
                print("Not found: "+line[0:-1]+"/"+year)
                continue

            # 写入文件
            with open(write_folder+"/"+line[0:7]+"_"+year+".json",'w') as fw:
                fw.write(str(r.json()))
                print("stored:"+line[0:-1]+"/"+year)

# 为所有股票下载所有数据，储存在 write_folder 的子目录中
# 将从year开始下载到上市的第一年或者year_first
def store_data_all(year="2022", year_first="2018", stocks_file="stock_test.txt", write_folder="./data"):
    # fileList = os.listdir(write_folder)
    with open(stocks_file) as f:
        for line in f:

            year_i = int(year)

            while True:
                
                url = "http://img1.money.126.net/data/hs/kline/day/history/"+str(year_i)+"/"+line[0:7]+".json"
                while True:
                    try:
                        r = requests.get(url)
                    except BaseException: # 请求失败,可能是因为被暂时屏蔽
                        print("Cannot connect to server!")
                    else:
                        break
                
                if r.status_code == 404: # 请求的股票已过了第一年上市
                    break

                # 写入文件
                with open(write_folder+"/"+line[0:7]+"_"+str(year_i)+".json",'w') as fw:
                    fw.write(str(r.json()))
                    print("stored:"+line[0:-1]+"/"+str(year_i))
                
                # 检查是否越过起始位置
                year_i -= 1
                if year_i < int(year_first):
                    break


# 保持A股上市以来的所有数据
if __name__ == "__main__":
    store_data_all(year="2022", year_first="2022", stocks_file="stocks.txt")
    # store_data(year="2019")
    # store_data(year="2018")
    # store_data(year="2017")
    # store_data(year="2016")
    # store_data(year="2015")
    # store_data(year="2014")
    # store_data(year="2013")
    # store_data(year="2012")
    # store_data(year="2011")
    # store_data(year="2010")
    # store_data(year="2009")
    # store_data(year="2008")
    # store_data(year="2007")
    # store_data(year="2006")
    # store_data(year="2005")
    # store_data(year="2004")
    # store_data(year="2003")
    # store_data(year="2002")
    # store_data(year="2001")
    # store_data(year="2000")
    # store_data(year="1999")
    # store_data(year="1998")
    # store_data(year="1997")
    # store_data(year="1996")
    # store_data(year="1995")
    # store_data(year="1994")
    # store_data(year="1993")
    # store_data(year="1992")
    # store_data(year="1991")
    # store_data(year="1990")