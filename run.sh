#! /bin/bash
echo "RSI strategy starts ..."
echo "Cleaning up ..."
rm ./today_strategy.txt
echo "Downloading data ... (may take 10 minutes)"
python3 ./store_data_tencent.py
echo "Calculating the buy point ... (may take 10 minutes)"
python3 ./daily_rsi_strategy_select_tencent.py > today_strategy.txt
echo "Successfully Done!"
echo ""
echo "------------------------------------------------- Strategy Report -------------------------------------------------"
echo ""
cat ./today_strategy.txt
echo ""
echo "You can also check out the strategy output in today_strategy.txt"
echo "Press Ctrl-C to quit"
while true; do
    sleep 10
done
