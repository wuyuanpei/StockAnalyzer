# StockAnalyzer
StockAnalyzer is a python analyzer of stock market, which provides many functions from data downloading, K-line drawing, to stock recommendation in China stock market.

## Files
Currently, we use tencent stock data https://web.ifzq.gtimg.cn/appstock/app/fqkline
- ``store_data_tencent.py``: download data from the tencent API
- ``daily_rsi_strategy_select_tencent.py``: show the stocks that the rsi strategy recommend (i.e., buy point)
- ``daily_rsi_strategy_sell_tencent.py``: test whether to sell the stocks recorded in ``stock_sell_tencent.txt`` (i.e., sell point)
- ``daily_rsi_strategy_draw_tencent.py``: draw the recent price and rsi of the specified stock

There are many other files that provide more functions regarding K-line and other APIs.

## Workflow
```
$ python ./store_data_tencent.py
$ python ./daily_rsi_strategy_select_tencent.py
$ python ./daily_rsi_strategy_draw_tencent.py sh600000
```
