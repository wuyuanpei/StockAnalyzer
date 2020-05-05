# 判断k线性质
# start:    k线开盘价
# end:      k线收盘价
# return: 
#   0 十字星
#   1, 2, 3 小,中,大阳线
#  -1,-2,-3 小,中,大阴线
def identify_line(start, end):
    rate = (end - start)/start * 100
    boundary = [0.5, 1.5, 3.5] # k线长度,注意它不等于涨幅
    if rate >= boundary[2]:
        return 3
    elif rate >= boundary[1]:
        return 2
    elif rate >= boundary[0]:
        return 1
    elif rate <= -boundary[2]:
        return -3
    elif rate <= -boundary[1]:
        return -2
    elif rate <= -boundary[0]:
        return -1
    else:
        return 0

# k线颜色
k_line_colors = ["yellow","tomato","red","darkred","darkgreen","limegreen","greenyellow"]

# 根据k线性质,返回颜色
# line_type: 
#   0 十字星
#   1, 2, 3 小,中,大阳线
#  -1,-2,-3 小,中,大阴线
# return: 
#   yellow 十字星
#   red 小,中,大阳线
#   green 小,中,大阴线
def color_line(line_type):
    return k_line_colors[line_type]

# 基本的加法/列表拼接统计方法
# stat:     历史数据
# data:     新数据
# return:   新统计数据
def add_op(stat, data):
    return stat + data

# 将历史数据数组与新数据数组每个元素求和
# stat:     历史数据
# data:     新数据
# return:   新统计数组
def add_list_op(stat, data):
    for i in range(len(stat)):
        stat[i] += data[i]
    return stat

# 返回5天的大致趋势
# end:  5天的收盘价
# return:   +1涨势 -1跌势 0波动势
def trend(end1, end2, end3, end4, end5):
    mean = (end1 + end2 + end3 + end4 + end5)/5
    if end1 < end2 and end2 < mean and end4 > mean and end5 > mean:
        return 1
    elif end1 > end2 and end2 > mean and end4 < mean and end5 < mean:
        return -1
    else:
        return 0