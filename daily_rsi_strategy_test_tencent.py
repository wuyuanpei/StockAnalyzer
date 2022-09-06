from daily_rsi_strategy_tencent import get_df_price
from daily_rsi_strategy_tencent import get_rsi
from daily_rsi_strategy_tencent import daily_implement_rsi_strategy

stock_names = []
stocks_file="stock_test_tencent.txt"
with open(stocks_file) as f:
    for line in f:
        stock_names.append(line[0:8])

all_year_rate = 0.0
all_rate = 0
all_hold_days = 0

num_stocks = 0

for stockname in stock_names:
    df_price = get_df_price(stockname)
    if len(df_price) == 0:
        continue

    df_price['rsi'] = get_rsi(df_price['closeprice'], 6) 
    # df_price = df_price.dropna()
    buy_price, sell_price, rsi_signal, trend_signal = daily_implement_rsi_strategy(df_price['closeprice'], df_price['rsi'])

    num_stocks += 1

    days = len(rsi_signal)
    if sum(rsi_signal) != 0:
        for i in range(days):
            if rsi_signal[days - i - 1] == 1:
                rsi_signal[days - i - 1] = 0
                buy_price[days - i - 1] = 0.0
                break

    assert sum(rsi_signal) == 0

    tradings = []
    
    buy_i = 0
    buy_p = 0.0
    for i in range(days):
        if rsi_signal[i] == 1:
            buy_i = i
            buy_p = buy_price[i]
        if rsi_signal[i] == -1:
            hold_days = i - buy_i
            profit = sell_price[i] - buy_p
            rate = profit/buy_p
            tradings.append((hold_days, profit, rate))

    print("{}: ".format(stockname))
    total_hold_days = 0.00000000001
    total_profit = 0.0
    total_rate = 1
    for hold_days, profit, rate in tradings:
        total_hold_days += hold_days
        total_rate *= (1 + rate)
        total_profit += profit
        print("\t(持股天数：{:.0f},\t盈利(元):{:.2f},\t收益：{:.2f}%,\t年化收益：{:.2f}%)".format(hold_days, profit, rate * 100, rate * 100 * 236 / hold_days))
    
    print("总持股天数：{:.0f},\t总盈利(元):{:.2f},\t总收益：{:.2f}%,\t总年化收益：{:.2f}%\n".format(total_hold_days, total_profit, (total_rate - 1) * 100, (total_rate - 1) * 100 * 236 / total_hold_days))
    
    all_year_rate += (total_rate - 1) * 100 * 236 / total_hold_days
    all_hold_days += total_hold_days
    all_rate += (total_rate - 1) * 100
    
print("平均每只股票持股天数：{:.2f}\t平均每只股票收益：{:.2f}%\t平均每只股票年化收益：{:.2f}%\n".format(all_hold_days/num_stocks, all_rate/num_stocks, all_year_rate/num_stocks))