from daily_rsi_strategy_tencent import get_df_price
from daily_rsi_strategy_tencent import get_rsi
from daily_rsi_strategy_tencent import daily_implement_rsi_strategy

stock_names = []
stocks_file="stock_test_tencent.txt"
with open(stocks_file) as f:
    for line in f:
        stock_names.append(line[0:8])

buy_list_last_day = []
buy_list_today = []

for stockname in stock_names:
    df_price = get_df_price(stockname)
    if len(df_price) == 0:
        continue
    df_price['rsi'] = get_rsi(df_price['closeprice'], 6) 
    # df_price = df_price.dropna()
    buy_price, sell_price, rsi_signal, trend_signal = daily_implement_rsi_strategy(df_price['closeprice'], df_price['rsi'])
    
    # not enough data
    if len(rsi_signal) < 10:
        continue

    if rsi_signal[-2] == 1:
        buy_list_last_day.append(stockname)

    if rsi_signal[-1] == 1:
        buy_list_today.append(stockname)

buy_list_last_day_good = dict()
with open("results_tencent.txt") as f:
    idx = 0
    switch = False
    for line in f:
        
        if line.find(buy_list_last_day[idx]) != -1:
            switch = True

        pos = line.find("总年化收益：")
        
        if switch and pos != -1:
            buy_list_last_day_good[buy_list_last_day[idx]] = float(line[pos + 6:-2])
            idx += 1
            switch = False

            if idx >= len(buy_list_last_day):
                break

print("yesterday:{}".format(sorted(buy_list_last_day_good.items(),key=lambda s:s[1])))


buy_list_today_good = dict()
with open("results_tencent.txt") as f:
    idx = 0
    switch = False
    for line in f:
        
        if line.find(buy_list_today[idx]) != -1:
            switch = True

        pos = line.find("总年化收益：")
        
        if switch and pos != -1:
            buy_list_today_good[buy_list_today[idx]] = float(line[pos + 6:-2])
            idx += 1
            switch = False

            if idx >= len(buy_list_today):
                break

print("today:{}".format(sorted(buy_list_today_good.items(),key=lambda s:s[1])))