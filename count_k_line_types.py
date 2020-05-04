from stats import stats
from utils import identify_line
from utils import k_line_colors
from utils import add_list_op
import sys
import matplotlib.pyplot as plt
import matplotlib
# 设置中文字体和负号正常显示
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 统计数据中出现的每种种类k线的数量
# dict:     数据点
# return:   统计数组 ["十字星","短红棒","中红棒","长红棒","长黑棒","中黑棒","短黑棒"]
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



# 画出(某年)(某只)股票的k线类型统计
if __name__ == "__main__":
    labels = ["十字星","短红棒","中红棒","长红棒","长黑棒","中黑棒","短黑棒"]
    try:
        if len(sys.argv) > 3:
            print("usage: python count_k_line_types.py [year]/- [id]")
        elif len(sys.argv) == 1:
            items = stats("./data", stat_op = add_list_op, data_fn=count_klinetypes, id=None, year=None)
            plt.bar(left=range(len(items)), width=0.8, height=[i/sum(items) for i in items], color=k_line_colors)
            plt.title("All Stock Data in All Years")
        elif len(sys.argv) == 2:
            items = stats("./data", stat_op = add_list_op, data_fn=count_klinetypes, id=None, year=sys.argv[1])
            plt.bar(left=range(len(items)), width=0.8, height=[i/sum(items) for i in items], color=k_line_colors)
            plt.title("All Stock Data in "+sys.argv[1])
        elif len(sys.argv) == 3 and sys.argv[1] == '-':
            items = stats("./data", stat_op = add_list_op, data_fn=count_klinetypes, id=sys.argv[2], year=None)
            plt.bar(left=range(len(items)), width=0.8, height=[i/sum(items) for i in items], color=k_line_colors)
            plt.title(sys.argv[2]+" in All Years")
        else:
            items = stats("./data", stat_op = add_list_op, data_fn=count_klinetypes, id=sys.argv[2], year=sys.argv[1])
            plt.bar(left=range(len(items)), width=0.8, height=[i/sum(items) for i in items], color=k_line_colors)
            plt.title(sys.argv[2]+" in "+sys.argv[1])

        plt.xticks(range(len(items)), labels)
        plt.show()
    except BaseException:
        print("Stock/Year not found or invalid!")