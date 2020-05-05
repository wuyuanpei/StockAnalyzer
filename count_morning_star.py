from stats import stats
from utils import identify_line
from utils import add_op
import sys

# 晨星识别参数
down_scale = 1.25 # 允许影线两端之差超过实体两端的倍数

# 统计参数:如果是晨星在下一天开盘价买入
stats_days = 3 # 第stats_days天在开盘价卖出

# 统计数据中出现的晨星 返回最后一天的位置的列表
# dict:     数据点
# return:   统计
def count_morning_star(dict):
    # 数据天数
    num = len(dict["data"])

    # 储存在当年里晨星的最后一天的位置的列表
    data_stat = []
    # 迭代数据点
    for i in range(2,num):
        day1 = dict["data"][i-2]
        day2 = dict["data"][i-1]
        day3 = dict["data"][i]

        start1 = day1[1]
        end1 = day1[2]
        highest1 = day1[3]
        lowest1 = day1[4]
        hand1 = day1[5]
        # 第一天长/中黑棒
        if not (identify_line(start1, end1) <= -2 and (highest1-lowest1) < (down_scale * (start1 - end1))):
            continue

        start2 = day2[1]
        end2 = day2[2]
        hand2 = day2[5]
        # 第二天跳空低开形成一十字星或小红棒或小黑棒
        k_line_type2 = identify_line(start2, end2)
        if not (max(start2, end2) < end1 and (k_line_type2 == 0 or k_line_type2 == 1 or k_line_type2 == -1)):
            continue

        
        start3 = day3[1]
        end3 = day3[2]
        highest3 = day3[3]
        lowest3 = day3[4]
        hand3 = day3[5]
        # 第三天跳空高开中长阳线
        if not (identify_line(start3, end3) >= 2 and start3 > max(start2, end2) and (highest3-lowest3) < (down_scale * (end3 - start3))):
            continue

        # # 第三天的收盘价高出第一天的开盘价
        # if not (end3 > start1):
        #     continue
        
        # # 明显更多的成交量
        # if not(hand3 > hand1 + hand2):
        #     continue
        
        # 统计参数
        if i < num - stats_days:
            # 比较第stats_days的开盘价和下一天的开盘价
            if dict["data"][i+stats_days][1] > dict["data"][i+1][1]:
                data_stat.append(dict["name"]+"/"+dict["symbol"]+"/"+dict["data"][i][0]+"/1")
            else:
                data_stat.append(dict["name"]+"/"+dict["symbol"]+"/"+dict["data"][i][0]+"/0")
        else:
            data_stat.append(dict["name"]+"/"+dict["symbol"]+"/"+dict["data"][i][0]+"/-")
    
    return data_stat

# 画出(某年)(某只)股票的晨星统计
if __name__ == "__main__":
    if len(sys.argv) > 3:
        print("usage: python count_morning_star.py [year]/- [id]")
    elif len(sys.argv) == 1:
        items = stats("./data", stat_op = add_op, data_fn=count_morning_star, id=None, year=None)
    elif len(sys.argv) == 2:
        items = stats("./data", stat_op = add_op, data_fn=count_morning_star, id=None, year=sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[1] == '-':
        items = stats("./data", stat_op = add_op, data_fn=count_morning_star, id=sys.argv[2], year=None)
    else:
        items = stats("./data", stat_op = add_op, data_fn=count_morning_star, id=sys.argv[2], year=sys.argv[1])

    # 打印统计结果
    count_win = 0
    count_lose = 0
    for i in range(len(items)):
        print(items[i])
        if items[i][-1] == "1":
            count_win += 1
        elif items[i][-1] == "0":
            count_lose += 1

    print("Number of Morning Star(s): "+str(len(items)))
    print("赚钱 vs. 亏钱: "+str(count_win)+":"+str(count_lose))