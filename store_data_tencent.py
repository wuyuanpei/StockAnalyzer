import requests
import time

# 为所有股票下载所有数据，储存在 write_folder 目录中
def store_data_all(stocks_file="stock_test_tencent.txt", write_folder="./tencent_data"):
    # fileList = os.listdir(write_folder)
    with open(stocks_file) as f:
        for line in f:
                
            url = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=" + line[0:8].lower() + ",day,2020-1-1," + time.strftime("%Y-%m-%d") + ",1000,qfq"
                
            try:
                r = requests.get(url)
            except BaseException: # 请求失败,可能是因为被暂时屏蔽
                print("Cannot connect to server for {}!".format(line[0:8]))
                continue
                
            if r.status_code == 404 or r.status_code == 403:
                print("Data cannot be found for {}!".format(line[0:8]))
                continue
                

            # 写入文件
            with open(write_folder+"/"+line[0:8]+".json",'w') as fw:
                fw.write(str(r.json()))
                print("stored:"+line[0:8])


# 保持A股上市以来的所有数据
if __name__ == "__main__":
    store_data_all()
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