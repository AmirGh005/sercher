import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import yfinance as yf

# دانلود داده های قیمت اتریوم از Yahoo Finance
start_date = "2024-09-04"  # تاریخ شروع
end_date = "2024-09-18"  # تاریخ پایان
eth_data = yf.download('ETH-USD', start=start_date, end=end_date,interval="5m")

# نمایش چند ردیف از داده ها
print("نمونه‌ای از داده‌های قیمت اتریوم:")
print(eth_data.head())

# اضافه کردن ستون های متغیرهای جدید مثل میانگین متحرک (moving average)
eth_data['MA_5'] = eth_data['Close'].rolling(window=5).mean()
eth_data['MA_15'] = eth_data['Close'].rolling(window=15).mean()
eth_data['Volatility'] = eth_data['Close'].rolling(window=5).std()

# حذف مقادیر NaN
eth_data = eth_data.dropna()

# متغیرهای ویژگی و هدف
X = eth_data[['MA_5', 'MA_15', 'Volatility']]
y = eth_data['Close']

# تقسیم داده به مجموعه آموزشی و تست
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# مدل Random Forest برای پیش‌بینی قیمت اتریوم
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# پیش بینی قیمت بر اساس داده تست
y_pred = model.predict(X_test)

# ارزیابی مدل
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nگزارش عملکرد مدل:")
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# نمایش نتایج پیش‌بینی
plt.figure(figsize=(10,6))
plt.plot(y_test.index, y_test, label='Actual Price')
plt.plot(y_test.index, y_pred, label='Predicted Price')
plt.title('Actual vs Predicted Ethereum Price')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()

# گزارش از وضعیت کنونی قیمت اتریوم
latest_eth = yf.download('ETH-USD', period='1d')

current_price = latest_eth['Close'].values[-1]
print(f"\nقیمت کنونی اتریوم: {current_price} USD")

# بررسی وضعیت نوسانات بر اساس عملکرد مدل
if r2 > 0.7:
    print("algorithm")
else:
    print("not algorithm")
