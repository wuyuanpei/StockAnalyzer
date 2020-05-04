import matplotlib.pyplot as plt
from utils import *
from stats import stats

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
    items = stats("./data", stat_op = add_klinetypes_counts, data_fn=count_klinetypes,id=None,year=None)
    plt.bar(range(len(items)),items, color=k_line_colors, tick_label=["star","short r","middle r","long r","long g","middle g","short g"])
    plt.show()


        