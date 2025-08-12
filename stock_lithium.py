import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# 下载股票数据（确保索引为单层）
stock = yf.download('1211.HK', start='2025-01-01', end='2025-06-30')
stock.columns = stock.columns.droplevel(1)
stock = stock.reset_index()  # 重置索引并保留日期列
stock["date"] = pd.to_datetime(stock["Date"])
stock = stock[["date", "Close"]]

# 读取锂价数据（单层索引）
lithium_price = pd.read_csv('lithium_data_2025H1_fixed.csv', parse_dates=['date'])

# 合并前统一索引层级（关键修复）
merged_data = pd.merge(
    lithium_price,
    stock, 
    on='date',
    how='inner'
)   

# 计算收益率
merged_data['锂价收益率'] = merged_data['spot_price'].pct_change() * 100
merged_data['股价收益率'] = merged_data['Close'].pct_change() * 100

# 验证结果
print(merged_data[['date', 'spot_price', 'Close', '锂价收益率', '股价收益率']].head())

#显示描述性统计分析
stats = merged_data[['spot_price', '锂价收益率']].describe()
print(stats)

# 30日滚动波动率（标准差）
merged_data['锂价波动率'] = merged_data['锂价收益率'].rolling(window=30).std()
print(merged_data['锂价波动率'])


from statsmodels.tsa.seasonal import STL
stl = STL(merged_data['spot_price'], period=90)  # 季度周期
result = stl.fit()
result.plot()  # 可视化趋势、季节性与残差
plt.show()











