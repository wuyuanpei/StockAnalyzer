import pandas as pd
import json

# 读取 year_first 到 year 的所有数据并合并成 pd.DataFrame
def get_df_price(stock, year_first=2018, year=2022, folder="./data"):
    
    ends = []

    year_i = year_first

    while True:
        # 打开本地文件
        try:
            file = open(folder + "/" + stock + "_" + str(year_i) + ".json")
        except BaseException:
            if year_i > year:
                break
            else:
                year_i += 1
                continue

        # 将数据转换成标准的json文件
        jstring = file.read().replace("\'","\"")
        response_dict = json.loads(jstring)

        # 数据天数
        num = len(response_dict["data"])

        for i in range(num):
            day = response_dict["data"][i]
            end = day[2]
            ends.append(end)

        year_i += 1

        if year_i > year:
            break
    
    return pd.DataFrame({'closeprice':ends})

# 根据价格计算rsi
def get_rsi(price, lookback):
    ret = price.diff()
    up = []
    down = []
    for i in range(len(ret)):
        if ret[i] < 0:
            up.append(0)
            down.append(ret[i])
        else:
            up.append(ret[i])
            down.append(0)
    up_series = pd.Series(up)
    down_series = pd.Series(down).abs()
    up_ewm = up_series.ewm(com = lookback - 1, adjust = False).mean()
    down_ewm = down_series.ewm(com = lookback - 1, adjust = False).mean()
    rs = up_ewm/down_ewm
    rsi = 100 - (100 / (1 + rs))
    rsi_df = pd.DataFrame(rsi).rename(columns = {0:'rsi'}).set_index(price.index)
    rsi_df = rsi_df.dropna()
    rsi_df = rsi_df[~rsi_df['rsi'].isin([0])]
    rsi_df = rsi_df[~rsi_df['rsi'].isin([100])]
    return rsi_df

# 策略：根据价格和rsi统计买入卖出点和买入卖出价格
def daily_implement_rsi_strategy(prices, rsi): 
    
    WINDOW_SIZE = 50
    BOUNDARY = 0.02
    
    bought = False

    buy_price = []
    sell_price = []
    rsi_signal = []
    trend_signal = []
    
    buy_count = 0
    sell_count = 0

    for i in range(len(prices)):
        
        if i == 0:
            buy_price.append(0)
            sell_price.append(0)
            rsi_signal.append(0)
            trend_signal.append(0)
            continue
        
        if i - WINDOW_SIZE < 0:
            start = 0
        else:
            start = i - WINDOW_SIZE
            
        window_highest = max(prices[start:i])
        window_lowest = min(prices[start:i])
        window_mean = sum(prices[start:i]) / len(prices[start:i])
        
        gt_lowest = False
        lt_highest = False
        
        if prices[i] > window_lowest * (1 + BOUNDARY):
            gt_lowest = True
            
        if prices[i] < window_highest * (1 - BOUNDARY):
            lt_highest = True

#         if prices[i] > window_mean * (1 + BOUNDARY):
#             gt_lowest = True
            
#         if prices[i] < window_mean * (1 - BOUNDARY):
#             lt_highest = True
            
        if gt_lowest and not lt_highest:
            trend = 1
        elif lt_highest and not gt_lowest:
            trend = -1
        else:
            trend = 0
            
        trend_signal.append(trend)

        if trend == 1:
            up_bar = 90
            down_bar = 40
        elif trend == -1:
            up_bar = 60
            down_bar = 10 
        else:
            up_bar = 80
            down_bar = 20
    
        if (rsi[i-1] < down_bar and rsi[i] >= down_bar and not bought):
            buy_price.append(prices[i])
            sell_price.append(0)
            rsi_signal.append(1)
            buy_count += 1
            bought = True
        
        elif (rsi[i-1] > up_bar and rsi[i] <= up_bar and bought):
            buy_price.append(0)
            sell_price.append(prices[i])
            rsi_signal.append(-1)
            sell_count += 1
            bought = False
            
        else:
            buy_price.append(0)
            sell_price.append(0)
            rsi_signal.append(0)
            
            
    return buy_price, sell_price, rsi_signal, trend_signal