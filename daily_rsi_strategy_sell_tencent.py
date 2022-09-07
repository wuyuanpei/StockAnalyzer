from daily_rsi_strategy_tencent import get_df_price
from daily_rsi_strategy_tencent import get_rsi
from daily_rsi_strategy_tencent import daily_implement_rsi_strategy

stock_names = []
stocks_file="stock_sell_tencent.txt"
with open(stocks_file) as f:
    for line in f:
        stock_names.append(line[0:8])

sell_list_last_day = []
sell_list_today = []

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

    if rsi_signal[-2] == -1:
        sell_list_last_day.append(stockname)

    if rsi_signal[-1] == -1:
        sell_list_today.append(stockname)

print("sell_list_last_day:{}".format(sell_list_last_day))
print("sell_list_today:{}".format(sell_list_today))