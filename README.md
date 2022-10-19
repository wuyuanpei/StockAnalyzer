# StockAnalyzer
StockAnalyzer is a python analyzer of stock market, which provides many functions from data downloading, K-line drawing, to stock recommendation in China stock market. Currently, we are only using the strategy based on [RSI indicator](https://en.wikipedia.org/wiki/Relative_strength_index), as it is tested effective in our trading history.

## Files
Currently, we use tencent stock data https://web.ifzq.gtimg.cn/appstock/app/fqkline
- ``stock_test_tencent.txt``: the list of stock indices to download
- ``stock_sell_tencent.txt``: the list of stock indices to test sell point
- ``results_tencent.txt``: the history decisions of the rsi strategy

- ``store_data_tencent.py``: download stock data specified in ``stock_test_tencent.txt`` from the tencent API and store them into ``./tencent_data/``
- ``daily_rsi_strategy_select_tencent.py``: show the stocks that the rsi strategy recommend (i.e., buy point). The results are sorted based on the history decision stored in ``results_tencent.txt``
- ``daily_rsi_strategy_sell_tencent.py``: test whether to sell the stocks recorded in ``stock_sell_tencent.txt`` (i.e., sell point)
- ``daily_rsi_strategy_draw_tencent.py``: draw the recent price and rsi of the specified stock
- ``daily_rsi_strategy_test_tencent.py``: store history decisions of the rsi strategy (in ``results_tencent.txt``)
- ``daily_rsi_strategy_test_next_tencent.py``: store history price change after buying the stock in the next ``WIN_DAY`` days. Data is stored in ``winX_results_tencent.txt`` when ``WIN_DAY=X``

There are many other files that provide more functions regarding K-line, machine learning, and other APIs. However, currenly only the rsi strategy has reasonable profits.

## Workflow
You may first need to install the necessary packets:
```
$ pip install pandas
$ pip install matlplotlib
```
When you would like to buy stocks, you can download data, see the recommendation, and check the graph if necessary.
```
$ mkdir tencent_data
$ python3 ./store_data_tencent.py
$ python3 ./daily_rsi_strategy_select_tencent.py
$ python3 ./daily_rsi_strategy_draw_tencent.py sh600000
```
When you would like to sell stocks, you can first register the stock indices in ``stock_sell_tencent.txt`` and then run:
```
$ python3 ./daily_rsi_strategy_sell_tencent.py
```
Also, you would like to run the following commands regularly to store the recent decisions and data about the strategy:s
```
$ python3 ./daily_rsi_strategy_test_tencent.py > results_tencent.txt

# when WIN_DAY is set to X
$ python3 ./daily_rsi_strategy_test_next_tencent.py > winX_results_tencnt.txt
```