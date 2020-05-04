import matplotlib.pyplot as plt
import matplotlib
from utils import *
from stats import stats

# 设置中文字体和负号正常显示
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

def count_klinetypes(dict):
    # 数据天数
    num = len(dict["data"])

    # 储存在当年里每种k线的出现次数
    data_stat = [0,0,0,0,0,0,0]
    # 迭代数据点
    for i in range(num):
        day = dict["data"][i]
        start = day[1]
        end = day[2]

        # 查找k线对应的种类,并加入统计
        line_type = identify_line(start, end)
        data_stat[line_type] += 1
    
    return data_stat

def add_klinetypes_counts(stat, data):
    for i in range(7):
        stat[i] += data[i]
    return stat

if __name__ == "__main__":

    labels = ["十字星","短红棒","中红棒","长红棒","长黑棒","中黑棒","短黑棒"]

    items = stats("./data", stat_op = add_klinetypes_counts, data_fn=count_klinetypes, id=None, year="2020")
    plt.bar(left=range(len(items)), width=0.15, height=[i/sum(items) for i in items], color="red", label="2020")

    items = stats("./data", stat_op = add_klinetypes_counts, data_fn=count_klinetypes, id=None, year="2019")
    plt.bar(left=[i + 0.15 for i in range(len(items))], width=0.15, height=[i/sum(items) for i in items], color="orange", label="2019")
    
    items = stats("./data", stat_op = add_klinetypes_counts, data_fn=count_klinetypes, id=None, year="2018")
    plt.bar(left=[i + 0.3 for i in range(len(items))], width=0.15, height=[i/sum(items) for i in items], color="green", label="2018")

    items = stats("./data", stat_op = add_klinetypes_counts, data_fn=count_klinetypes, id=None, year="2017")
    plt.bar(left=[i + 0.45 for i in range(len(items))], width=0.15, height=[i/sum(items) for i in items], color="blue", label="2017")

    items = stats("./data", stat_op = add_klinetypes_counts, data_fn=count_klinetypes, id=None, year="2016")
    plt.bar(left=[i + 0.6 for i in range(len(items))], width=0.15, height=[i/sum(items) for i in items], color="purple", label="2016")
    
    plt.xticks([index + 0.3 for index in range(len(items))], labels)

    plt.legend()
    plt.show()
