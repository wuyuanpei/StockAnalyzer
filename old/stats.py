import requests
import matplotlib.pyplot as plt
import sys
import json
import os
from tqdm import tqdm

# 根据输入的规则和统计方法统计数据
# foldername:   数据所在文件夹
# stat_op:      统计方法, stat = lambda(stat,data)
#                   stat: 已经统计的结果
#                   data: 新数据的统计
# data_fn:      对于一个数据点的统计规则 data = lambda(dict)
#                   dict: 数据字典
# year:         数据年份
# id:           股票代码
# v:            verbose mode, True or False
def stats(foldername, stat_op, data_fn, id=None, year=None, v=True):
    fileList = os.listdir(foldername)
    # 如果年份和股票代码被声明,则只保留符合条件的数据
    if year is not None:
        fileList = list(filter(lambda filename:filename[8:12]==year, fileList))
    if id is not None:
        fileList = list(filter(lambda filename:filename[0:7]==id, fileList))
    
    # 文件列表为空
    if not fileList and v:
        print("No such file(s) found!")

    # 统计变量
    stat = None
    # 迭代文件
    if v:
        fns = tqdm(fileList)
    else:
        fns = fileList
    for filename in fns:
        file = open(foldername+"/"+filename)

        jstring = file.read().replace("\'","\"")
        response_dict = json.loads(jstring)

        # 将字典传入data_fn,并使用stat_op统计数据
        if stat is None:
            stat = data_fn(response_dict)
        else:
            stat = stat_op(stat, data_fn(response_dict))

    return stat

        

if __name__ == "__main__":
    items = stats("./data", stat_op = lambda stat,data: stat+data, data_fn=lambda x: 1,id=None,year=None)
    print("数据个数:"+str(items))




