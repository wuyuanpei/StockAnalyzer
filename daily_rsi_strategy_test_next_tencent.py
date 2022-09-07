from daily_rsi_strategy_tencent import get_df_price
from daily_rsi_strategy_tencent import get_rsi
from daily_rsi_strategy_tencent import daily_implement_rsi_strategy

WIN_DAY = 1

stock_names = []
stocks_file="stock_sell_tencent.txt"
with open(stocks_file) as f:
    for line in f:
        stock_names.append(line[0:8])

win_all = 0
lose_all = 0
price_diff_all = 0.0
for stockname in stock_names:
    df_price = get_df_price(stockname)
    if len(df_price) == 0:
        continue

    df_price['rsi'] = get_rsi(df_price['closeprice'], 6) 
    # df_price = df_price.dropna()
    buy_price, sell_price, rsi_signal, trend_signal = daily_implement_rsi_strategy(df_price['closeprice'], df_price['rsi'])

    days = len(rsi_signal)

    print("{}: ".format(stockname))

    win = 0
    lose = 0
    price_diff = 0.0
    for i in range(days - WIN_DAY):
        if rsi_signal[i] == 1:
            price_diff += df_price['closeprice'][i + WIN_DAY] - df_price['closeprice'][i]
            if df_price['closeprice'][i + WIN_DAY] > df_price['closeprice'][i]:
                win += 1
                print("\t赚 当日价格: {:.2f}\t次日价格: {:.2f}\t盈利: {:.2f}".format(df_price['closeprice'][i], df_price['closeprice'][i + WIN_DAY], df_price['closeprice'][i + WIN_DAY] - df_price['closeprice'][i]))
            else:
                lose += 1
                print("\t亏 当日价格: {:.2f}\t次日价格: {:.2f}\t亏损: {:.2f}".format(df_price['closeprice'][i], df_price['closeprice'][i + WIN_DAY], df_price['closeprice'][i] - df_price['closeprice'][i + WIN_DAY]))
    
    win_all += win
    lose_all += lose
    price_diff_all += price_diff
    print("盈利次数: {}\t亏损次数: {}\t胜率: {:.1f}%\t策略盈利: {:.2f}\n".format(win, lose, win / (win + lose + 0.00000000000000001) * 100, price_diff))

print("总盈利次数: {}\t总亏损次数: {}\t总胜率: {:.1f}%\t总策略盈利: {:.2f}".format(win_all, lose_all, win_all / (win_all + lose_all + 0.000000000000000001) * 100, price_diff_all))