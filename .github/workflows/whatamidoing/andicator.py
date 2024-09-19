import pandas as pd
import matplotlib.pyplot as plt
from ta.trend import SMAIndicator, MACD
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator

# خواندن داده‌ها
df = pd.read_csv('ETH-USD_hourly_data2.csv', parse_dates=['Datetime'])

# محاسبه اندیکاتورها
sma = SMAIndicator(df['Close'], window=14)
df['SMA'] = sma.sma_indicator()

macd = MACD(df['Close'])
df['MACD'] = macd.macd()
df['MACD_Signal'] = macd.macd_signal()

bollinger = BollingerBands(df['Close'], window=20, window_dev=2)
df['Bollinger_High'] = bollinger.bollinger_hband()
df['Bollinger_Low'] = bollinger.bollinger_lband()

rsi = RSIIndicator(df['Close'], window=14)
df['RSI'] = rsi.rsi()

# تحلیل روند با استفاده از ترکیب اندیکاتورها
def analyze_trend(row):
    if row['MACD'] > row['MACD_Signal'] and row['RSI'] > 50:
        return 'Up'
    elif row['MACD'] < row['MACD_Signal'] and row['RSI'] < 50:
        return 'Down'
    else:
        return 'Neutral'

df['Trend'] = df.apply(analyze_trend, axis=1)

# پیش‌بینی روند آینده
def forecast_trend(df, periods=5):
    forecast = []
    for i in range(len(df) - periods, len(df)):
        trend = analyze_trend(df.iloc[i])
        forecast.append(trend)
    return forecast

# تعداد دوره‌هایی که می‌خواهیم پیش‌بینی کنیم
future_periods = 5
forecasted_trends = forecast_trend(df, periods=future_periods)

# چاپ گزارش تحلیل روند آینده
print("تحلیل روند برای دوره‌های بعدی:")
for i, trend in enumerate(forecasted_trends):
    print(f"دوره {i + 1}: {trend}")

# رسم نمودار
plt.figure(figsize=(14, 10))

plt.plot(df['Datetime'], df['Close'], label='Close Price')
plt.plot(df['Datetime'], df['SMA'], label='SMA (14)', linestyle='--')
plt.plot(df['Datetime'], df['Bollinger_High'], label='Bollinger High', linestyle='--', color='red')
plt.plot(df['Datetime'], df['Bollinger_Low'], label='Bollinger Low', linestyle='--', color='green')

# مشخص کردن روندهای پیش‌بینی شده
for i in range(len(df)):
    if df['Trend'].iloc[i] == 'Up':
        plt.plot(df['Datetime'].iloc[i], df['Close'].iloc[i], marker='^', color='green', markersize=10)
    elif df['Trend'].iloc[i] == 'Down':
        plt.plot(df['Datetime'].iloc[i], df['Close'].iloc[i], marker='v', color='red', markersize=10)

plt.title('Technical Analysis with Advanced Indicators and Trend Forecast')
plt.xlabel('Datetime')
plt.ylabel('Price')
plt.legend()
plt.grid()
plt.show()
