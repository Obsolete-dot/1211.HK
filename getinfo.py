import akshare as ak
import pandas as pd

# 1. 获取期货数据（日期格式：YYYY-MM-DD）
futures_data = ak.futures_main_sina(
    symbol="LC0", start_date="20250101", end_date="20250630"
)[["日期", "收盘价"]].rename(columns={"日期": "date", "收盘价": "close_futures"})
futures_data["close_futures"] = futures_data["close_futures"].astype(float)

# 2. 获取现货数据（日期格式：YYYYMMDD）
spot_data = ak.futures_spot_price_daily(
    start_day="20250101", end_day="20250630", vars_list=["LC"]
)
spot_data = spot_data[["date", "spot_price"]]
    
# 关键修复：统一日期格式为 YYYY-MM-DD
futures_data["date"] = pd.to_datetime(futures_data["date"]).dt.strftime("%Y-%m-%d")
spot_data["date"] = pd.to_datetime(spot_data["date"], format="%Y%m%d").dt.strftime("%Y-%m-%d")  # 指定原始格式

# 3. 合并数据
merged_data = pd.merge(futures_data, spot_data, on="date", how="left")

# 4. 数据验证（检查缺失值）
print("现货缺失日期:", merged_data[merged_data["spot_price"].isna()]["date"].tolist())

# 5. 填充缺失值
merged_data["spot_price_ffill"] = merged_data["spot_price"].ffill()  # 前向填充值
merged_data["spot_price_bfill"] = merged_data["spot_price"].bfill()  # 后向填充值

#计算前后均值，仅填充原缺失位置
merged_data["spot_price_filled"] = merged_data["spot_price"].fillna(
    (merged_data["spot_price_ffill"] + merged_data["spot_price_bfill"]) / 2
)

#替换原列并清理临时列
merged_data["spot_price"] = merged_data["spot_price_filled"]
merged_data.drop(["spot_price_ffill", "spot_price_bfill", "spot_price_filled"], axis=1, inplace=True)

# 6. 保存结果
merged_data.to_csv("lithium_data_2025H1_fixed.csv", index=False)
print(f"数据已保存！缺失值数量: {merged_data['spot_price'].isna().sum()}")