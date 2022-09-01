from daily_rsi_strategy import get_df_price
from daily_rsi_strategy import get_rsi
from daily_rsi_strategy import daily_implement_rsi_strategy

stock_names = []
stocks_file="stocks.txt"
with open(stocks_file) as f:
    for line in f:
        stock_names.append(line[0:7])

buy_list = []

for stockname in stock_names:
    df_price = get_df_price(stockname)
    if len(df_price) == 0:
        continue
    df_price['rsi'] = get_rsi(df_price['closeprice'], 6) 
    # df_price = df_price.dropna()
    buy_price, sell_price, rsi_signal, trend_signal = daily_implement_rsi_strategy(df_price['closeprice'], df_price['rsi'])
    if rsi_signal[-1] == 1 or rsi_signal[-2] == 1:
        buy_list.append(stockname)

print(buy_list)