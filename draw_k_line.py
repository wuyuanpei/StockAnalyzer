import requests
import matplotlib.pyplot as plt
import sys
import json
from utils import *

# 画出某一股票某一年的k线图
# id:       股票的代号
# year:     年份
# foldername: None 使用在线API
#            "XX" 使用位于文件夹XX的本地文件
def draw_k_line(id, year="2020", foldername=None):
    # 在线API
    if foldername is None:
        url = "http://img1.money.126.net/data/hs/kline/day/history/"+year+"/"+id+".json"
        r = requests.get(url)
        # 找不到股票
        if r.status_code == 404:
            print("No such stock found!")
            return
        response_dict = r.json()
    else:
        # 打开本地文件
        try:
            file = open(foldername+"/"+id+"_"+year+".json")
        except BaseException:
            print("No such file!")
            return
        # 将数据转换成标准的json文件
        jstring = file.read().replace("\'","\"")
        response_dict = json.loads(jstring)

    # 数据天数
    num = len(response_dict["data"])

    # 窗口、坐标轴设定
    fig = plt.figure(figsize=(min(num/5, 17),5))
    ax = fig.add_subplot(111, axisbg="black")
    ax.set_xlim(0, num)

    # 记录最高点、最低点
    all_lowest = 100000000
    all_highest = 0
    idx_lowest = 0
    idx_highest = 0
    for i in range(num):
        day = response_dict["data"][i]
        start = day[1]
        end = day[2]
        highest = day[3]
        lowest = day[4]
        
        # 更新最低点 最高点
        if lowest < all_lowest:
            all_lowest = lowest
            idx_lowest = i
        if highest > all_highest:
            all_highest = highest
            idx_highest = i

        # 查找k线对应的种类 颜色
        line_type = identify_line(start, end)
        c = color_line(line_type)

        # 绘图
        if line_type > 0: # 红线
            rect = plt.Rectangle((i,start),0.75, end - start, color=c)
            ax.add_patch(rect)
            line = plt.Line2D((i+0.4,i+0.4),(lowest,highest), color=c)
            ax.add_line(line)
        else: # 绿线 黄线
            rect = plt.Rectangle((i,end),0.75, start - end, color=c)
            ax.add_patch(rect)
            line = plt.Line2D((i+0.4,i+0.4),(lowest,highest), color=c)
            ax.add_line(line)

    # 如果在最后一天,调整最高点最低点的显示位置
    if idx_lowest == num - 1:
        idx_lowest_d = num -2
    else:
        idx_lowest_d = idx_lowest
    if idx_highest == num - 1:
        idx_highest_d = num - 2
    else:
        idx_highest_d = idx_highest

    # 绘制最高点 最低点的值
    text=plt.Text(idx_lowest_d,all_lowest-(all_highest-all_lowest)/12,'%.2f'%all_lowest, color="white", fontsize=10)
    ax.add_artist(text)
    text=plt.Text(idx_highest_d,all_highest+(all_highest-all_lowest)/20,'%.2f'%all_highest, color="white", fontsize=10)
    ax.add_artist(text)

    # 设置y轴长度和图的标签
    ax.set_ylim(all_lowest - (all_highest-all_lowest)/5, all_highest + (all_highest-all_lowest)/5)
    plt.grid(axis="y",linestyle='--', color='grey')
    plt.title(response_dict["symbol"]+"/"+year)

    # 绘图 打印股票名称
    plt.show()
    print(response_dict["name"])

# 使用在线API画k线图
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python draw_k_line.py year id")
        # Examples
        draw_k_line("0000001", "2020")
        draw_k_line("0600536", "2020")
        draw_k_line("0601009", "2020")
    else:
        draw_k_line(sys.argv[2], sys.argv[1])
