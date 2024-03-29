import requests
import matplotlib.pyplot as plt
import matplotlib
import sys
import json
from utils import identify_line
from utils import color_line
from utils import trend

# 设置中文字体和负号正常显示
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 画出某一股票某一年的k线图,实际收盘价,实际和预测涨跌幅
# id:       股票的代号
# year:     年份
# foldername: "XX" 使用位于文件夹XX的本地文件
# prediction: 预测数组,包含每天的涨跌幅
def draw_results(id, year="2020", foldername="./data", prediction="None"):
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

    # 窗口 坐标轴设定
    plt.ioff()
    fig = plt.figure(figsize=(min(num/4, 19),10))
    ax = fig.add_subplot(2,1,1, fc="black")
    ax2 = fig.add_subplot(2,1,2, fc="black")
    ax.set_xlim(0, num)
    ax2.set_xlim(0, num)

    # 记录最高点 最低点 成交量  趋势
    all_lowest = 100000000
    all_highest = 0
    idx_lowest = 0
    idx_highest = 0
    colors = []
    trs = []
    ends = []
    rates = []

    for i in range(num):
        day = response_dict["data"][i]
        start = day[1]
        end = day[2]
        highest = day[3]
        lowest = day[4]
        ends.append(day[2])
        rates.append(day[6])

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
        
        # 交易量颜色 此时黄色是严格等于
        if end - start > 0:
            colors.append("red")
        elif end - start < 0:
            colors.append("green")
        else:
            colors.append("yellow")

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
        
        # 记录趋势标记
        if i > 3:
            trs.append(trend(response_dict["data"][i-4][2], \
                response_dict["data"][i-3][2], response_dict["data"][i-2][2], \
                response_dict["data"][i-1][2], end))

    # 绘制收盘价图和神经网络预测数据
    ax.plot(ends)
    ax2.plot(rates, color="orange")
    if prediction is not None:
        ax2.plot(prediction, color="red")

    # 绘制趋势标记
    for i in range(4, num):
        if trs[i-4] == 1:
            text=plt.Text(i,all_lowest-(all_highest-all_lowest)/5,"^", color="red", fontsize=20)
            ax.add_artist(text)
        elif trs[i-4] == -1:
            text=plt.Text(i,all_lowest-(all_highest-all_lowest)/5,"^", color="green", fontsize=20)
            ax.add_artist(text)

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
    ax.grid(axis="y",linestyle='--', color='grey')
    ax2.grid(axis="y",linestyle='--', color='grey')
    
    plt.title(response_dict["name"]+"/"+response_dict["symbol"]+"/"+year)
    
    # 绘图
    plt.show()
    

# 画
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python view.py year id")
        # Examples
        draw_results("0600536", "2020", prediction=None)
        draw_results("0601009", "2020", prediction=None)
    else:
        draw_results(sys.argv[2], sys.argv[1], prediction=None)
