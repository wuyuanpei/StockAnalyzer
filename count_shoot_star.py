from stats import stats
from utils import identify_line
from utils import add_op
import sys

# 射击之星识别参数
up_multiple = 2 # 上影线长度在实体的up_multiple倍数之上
down_multiple = 0.2 # 下影线长度在上影线长度的down_multiple倍数以内
hands_multiple = 1.5 # 成交量大于前一天的hands_multiple倍

# 统计参数:如果是射击之星在最后一天开盘价买入
stats_days = 3 # 第stats_days天在开盘价卖出

# 统计数据中出现的射击之星 返回最后一天的位置的列表
# dict:     数据点
# return:   统计
def count_shoot_star(dict):
    # 数据天数
    num = len(dict["data"])

    # 储存在当年里射击之星的最后一天的位置的列表
    data_stat = []
    # 迭代数据点
    for i in range(1,num):
        day1 = dict["data"][i-1]
        day2 = dict["data"][i]

        start1 = day1[1]
        end1 = day1[2]
        hands1 = day1[5]
        # 第一天长或中红棒
        if not (identify_line(start1, end1) >= 2):
            continue

        start2 = day2[1]
        end2 = day2[2]
        highest2 = day2[3]
        lowest2 = day2[4]
        hands2 = day2[5]
        k_line_type2 = identify_line(start2, end2)
        # 第二天长上影线 十字星或小棒
        if not (k_line_type2 == -1 and \
                        highest2 - max(start2, end2) > up_multiple * abs(start2-end2) and \
                        min(start2, end2) - lowest2 < down_multiple * (highest2 - max(start2, end2))):
            continue
        
        # 第二天成交量大于第一天成交量
        if not (hands2 > hands1 * hands_multiple):
            continue

        # 统计参数
        if i < num - stats_days:
            # 比较第stats_days的开盘价和最后一天的开盘价
            if dict["data"][i+stats_days][1] > start2:
                data_stat.append(dict["name"]+"/"+dict["symbol"]+"/"+dict["data"][i][0]+"/1")
            else:
                data_stat.append(dict["name"]+"/"+dict["symbol"]+"/"+dict["data"][i][0]+"/0")
        else:
            data_stat.append(dict["name"]+"/"+dict["symbol"]+"/"+dict["data"][i][0]+"/-")
    
    return data_stat

# 打印出(某年)(某只)股票的射击之星统计
if __name__ == "__main__":
    if len(sys.argv) > 3:
        print("usage: python count_shoot_star.py [year]/- [id]")
    elif len(sys.argv) == 1:
        items = stats("./data", stat_op = add_op, data_fn=count_shoot_star, id=None, year=None)
    elif len(sys.argv) == 2:
        items = stats("./data", stat_op = add_op, data_fn=count_shoot_star, id=None, year=sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[1] == '-':
        items = stats("./data", stat_op = add_op, data_fn=count_shoot_star, id=sys.argv[2], year=None)
    else:
        items = stats("./data", stat_op = add_op, data_fn=count_shoot_star, id=sys.argv[2], year=sys.argv[1])

    # 打印统计结果
    count_win = 0
    count_lose = 0
    for i in range(len(items)):
        print(items[i])
        if items[i][-1] == "1":
            count_win += 1
        elif items[i][-1] == "0":
            count_lose += 1

    print("Number of Shoot Star(s): "+str(len(items)))
    print("赚钱 vs. 亏钱: "+str(count_win)+":"+str(count_lose))