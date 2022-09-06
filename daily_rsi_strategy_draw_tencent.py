import numpy as np
import matplotlib.pyplot as plt
import sys
from daily_rsi_strategy_tencent import get_df_price
from daily_rsi_strategy_tencent import get_rsi
from daily_rsi_strategy_tencent import daily_implement_rsi_strategy


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python daily_rsi_strategy_draw_tencent.py id")
    else:
        stock = sys.argv[1]
        df_price = get_df_price(stock)

        print(df_price)

        df_price['rsi'] = get_rsi(df_price['closeprice'], 6) 
        # df_price = df_price.dropna()
        buy_price, sell_price, rsi_signal, trend_signal = daily_implement_rsi_strategy(df_price['closeprice'], df_price['rsi'])

        if sum(rsi_signal) != 0:
            days = len(rsi_signal)
            for i in range(days):
                if rsi_signal[days - i - 1] == 1:
                    rsi_signal[days - i - 1] = 0
                    #buy_price[days - i - 1] = 0.0
                    break

        assert sum(rsi_signal) == 0

        sum_profit = 0.0
        for i in range(len(sell_price)):
            sum_profit -= (sell_price[i] * rsi_signal[i] + buy_price[i] * rsi_signal[i])
            if sell_price[i] == 0.0:
                sell_price[i] = np.nan
            if buy_price[i] == 0.0:
                buy_price[i] = np.nan
    
        profit = sum_profit

        print("{}: {}".format(stock, profit))

        upper_bound = []
        lower_bound = []

        for i in trend_signal:
            if i == 0:
                upper_bound.append(80)
                lower_bound.append(20)
            if i == -1:
                upper_bound.append(60)
                lower_bound.append(10)
            if i == 1:
                upper_bound.append(90)
                lower_bound.append(40)
        
        ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
        ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 4, colspan = 1)
        ax1.plot(df_price['closeprice'], linewidth = 2.5, color = 'skyblue', label = 'CFGX')
        ax1.plot(df_price.index, buy_price, marker = '^', markersize = 7, color = 'green', label = 'BUY SIGNAL')
        ax1.plot(df_price.index, sell_price, marker = 'v', markersize = 7, color = 'red', label = 'SELL SIGNAL')
        ax1.set_title('RSI TRADE SIGNALS')
        ax2.plot(df_price['rsi'], color = 'orange', linewidth = 2)
        ax2.plot(upper_bound, linestyle = '--', color = 'grey', linewidth = 1.5)
        ax2.plot(lower_bound, linestyle = '--', color = 'grey', linewidth = 1.5)
        plt.show()