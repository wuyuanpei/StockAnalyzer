from stats import stats
from utils import trend
from utils import add_op
import sys


# 统计参数:如果是上升趋势在下一天开盘价买入
stats_days = 10 # 第stats_days天在收盘价卖出

# 统计数据中出现的上升 返回最后一天的位置的列表
# dict:     数据点
# return:   统计
def count_trend(dict):
    # 数据天数
    num = len(dict["data"])

    # 储存在当年里上升趋势的最后一天的位置的列表
    data_stat = []
    # 迭代数据点
    for i in range(6,num):
        day_1 = dict["data"][i-6]
        day0 = dict["data"][i-5]
        day1 = dict["data"][i-4]
        day2 = dict["data"][i-3]
        day3 = dict["data"][i-2]
        day4 = dict["data"][i-1]
        day5 = dict["data"][i]

        end_1 = day_1[2]
        end0 = day0[2]
        end1 = day1[2]
        end2 = day2[2]
        end3 = day3[2]
        end4 = day4[2]
        end5 = day5[2]

        # 连续3天有2次以上上升趋势
        if not(trend(end1,end2,end3,end4,end5) + trend(end0,end1,end2,end3,end4) + trend(end_1,end0,end1,end2,end3) > 2):
            continue

       # 统计参数
        if i < num - stats_days:
            # 比较第stats_days的收盘价和下一天的开盘价
            if dict["data"][i+stats_days][2] > dict["data"][i+1][1]:
                data_stat.append(dict["name"]+"/"+dict["symbol"]+"/"+dict["data"][i][0]+"/1")
            else:
                data_stat.append(dict["name"]+"/"+dict["symbol"]+"/"+dict["data"][i][0]+"/0")
        else:
            data_stat.append(dict["name"]+"/"+dict["symbol"]+"/"+dict["data"][i][0]+"/-")
    
    return data_stat

# 打印出(某年)(某只)股票的上升趋势统计
if __name__ == "__main__":
    if len(sys.argv) > 3:
        print("usage: python count_trend.py [year]/- [id]")
    elif len(sys.argv) == 1:
        items = stats("./data", stat_op = add_op, data_fn=count_trend, id=None, year=None)
    elif len(sys.argv) == 2:
        items = stats("./data", stat_op = add_op, data_fn=count_trend, id=None, year=sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[1] == '-':
        items = stats("./data", stat_op = add_op, data_fn=count_trend, id=sys.argv[2], year=None)
    else:
        items = stats("./data", stat_op = add_op, data_fn=count_trend, id=sys.argv[2], year=sys.argv[1])

    # 打印统计结果
    count_win = 0
    count_lose = 0
    for i in range(len(items)):
        if items[i][-1] == "1":
            count_win += 1
        elif items[i][-1] == "0":
            count_lose += 1
        if items[i][-1] == "-" and items[i][-5] == "5":
            print(items[i])
    print("Number of Positive Trend(s): "+str(len(items)))
    print("赚钱 vs. 亏钱: "+str(count_win)+":"+str(count_lose))