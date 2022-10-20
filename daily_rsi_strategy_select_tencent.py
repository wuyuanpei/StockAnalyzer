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
hold_list = []

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
        buy_list_last_day.append((stockname, buy_price[-2]))

    if rsi_signal[-1] == 1:
        buy_list_today.append((stockname, buy_price[-1]))

    for i in range(len(rsi_signal)):
        if rsi_signal[len(rsi_signal) - 1 -i] == -1 or i > 10:
            break
        elif rsi_signal[len(rsi_signal) - 1 -i] == 1:
            hold_list.append((stockname, i, df_price['closeprice'][len(rsi_signal) - 1 -i], df_price['closeprice'][len(rsi_signal) - 1]))

buy_list_last_day_good = dict()
if len(buy_list_last_day) > 0:
    with open("results_tencent.txt") as f:
        idx = 0
        switch = False
        for line in f:
        
            if line.find(buy_list_last_day[idx][0]) != -1:
                switch = True

            pos = line.find("总年化收益：")
        
            if switch and pos != -1:
                buy_list_last_day_good[buy_list_last_day[idx]] = float(line[pos + 6:-2])
                idx += 1
                switch = False

                if idx >= len(buy_list_last_day):
                    break

buy_list_today_good = dict()
if len(buy_list_today) > 0:
    with open("results_tencent.txt") as f:
        idx = 0
        switch = False
        for line in f:
        
            if line.find(buy_list_today[idx][0]) != -1:
                switch = True

            pos = line.find("总年化收益：")
        
            if switch and pos != -1:
                buy_list_today_good[buy_list_today[idx]] = float(line[pos + 6:-2])
                idx += 1
                switch = False

                if idx >= len(buy_list_today):
                    break



hold_list_good = dict()
if len(hold_list) > 0:
    with open("results_tencent.txt") as f:
        idx = 0
        switch = False
        for line in f:
        
            if line.find(hold_list[idx][0]) != -1:
                switch = True

            pos = line.find("总年化收益：")
        
            if switch and pos != -1:
                hold_list_good[hold_list[idx]] = float(line[pos + 6:-2])
                idx += 1
                switch = False

                if idx >= len(hold_list):
                    break

print("\n================================================= 10-day holding =================================================")
for k, v in sorted(hold_list_good.items(),key=lambda s:-s[1]):
    print("代码: {}\t\t历史年收: {}%\t\t持有天数: {}\t\t买价: {}\t\t现价: {}".format(k[0], v, k[1], k[2], k[3]))

print("\n=============================================== yesterday buypoint ===============================================")
for k, v in sorted(buy_list_last_day_good.items(),key=lambda s:-s[1]):
    print("代码: {}\t\t历史年收: {}%\t\t买价: {}".format(k[0], v, k[1]))

print("\n================================================= today buypoint =================================================")
for k, v in sorted(buy_list_today_good.items(),key=lambda s:-s[1]):
    print("代码: {}\t\t历史年收: {}%\t\t买价: {}".format(k[0], v, k[1]))