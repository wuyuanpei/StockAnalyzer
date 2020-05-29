from stats import stats
from utils import add_op
import sys
import numpy as np

# 利用stats将数据转换成array,可在之后转换成ndarray或tensor提供给神经网络模型
# dict:     数据点
# return:   array of shape (days, 6)
#           其中[i][0-5]依次为 day i 的 start, end, highest, lowest, hand, rate
def data_load(dict):

    # 数据天数
    num = len(dict["data"])

    # 储存数据点
    data_stat = []

    # 迭代数据点
    for i in range(num):
        day = dict["data"][i]
        data_stat.append(day[1:])
    
    return data_stat

# 将选定的年份与股票转换成ndarray
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python data_loader.py [year]/- id")
    if sys.argv[1] == '-':
        items = stats("./data", stat_op = add_op, data_fn=data_load, id=sys.argv[2], year=None)
    else:
        items = stats("./data", stat_op = add_op, data_fn=data_load, id=sys.argv[2], year=sys.argv[1])
    items = np.array(items)

    print(items[:-1,:].shape)