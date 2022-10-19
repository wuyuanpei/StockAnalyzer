import matplotlib.pyplot as plt
import matplotlib
from stats import stats
from count_k_line_types import count_klinetypes
from utils import add_list_op

# 设置中文字体和负号正常显示
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 画出五年k线类型数据统计
def draw_five_years_line_types_stats():

    labels = ["十字星","短红棒","中红棒","长红棒","长黑棒","中黑棒","短黑棒"]

    items = stats("./data", stat_op = add_list_op, data_fn=count_klinetypes, id=None, year="2020")
    plt.bar(left=range(len(items)), width=0.15, height=[i/sum(items) for i in items], color="red", label="2020")

    items = stats("./data", stat_op = add_list_op, data_fn=count_klinetypes, id=None, year="2019")
    plt.bar(left=[i + 0.15 for i in range(len(items))], width=0.15, height=[i/sum(items) for i in items], color="orange", label="2019")
    
    items = stats("./data", stat_op = add_list_op, data_fn=count_klinetypes, id=None, year="2018")
    plt.bar(left=[i + 0.3 for i in range(len(items))], width=0.15, height=[i/sum(items) for i in items], color="green", label="2018")

    items = stats("./data", stat_op = add_list_op, data_fn=count_klinetypes, id=None, year="2017")
    plt.bar(left=[i + 0.45 for i in range(len(items))], width=0.15, height=[i/sum(items) for i in items], color="blue", label="2017")

    items = stats("./data", stat_op = add_list_op, data_fn=count_klinetypes, id=None, year="2016")
    plt.bar(left=[i + 0.6 for i in range(len(items))], width=0.15, height=[i/sum(items) for i in items], color="purple", label="2016")
    
    plt.xticks([index + 0.3 for index in range(len(items))], labels)

    plt.legend()
    plt.show()

# 画出5年的k线类型统计
if __name__ == "__main__":
    draw_five_years_line_types_stats()