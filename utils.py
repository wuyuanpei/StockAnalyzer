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

k_line_colors = ["yellow","tomato","red","darkred","darkgreen","limegreen","greenyellow"] # k线颜色
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