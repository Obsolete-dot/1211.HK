import akshare as ak

import pandas as pd
import yfinance as yf
stock = yf.download('1211.HK', start='2025-01-01', end='2025-06-30')
stock = stock.reset_index()  # 重置索引并保留日期列
stock["date"] = pd.to_datetime(stock["Date"]).dt.strftime("%Y-%m-%d")
stock = stock[["date", "Close"]]
print(stock)