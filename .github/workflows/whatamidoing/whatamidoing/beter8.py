import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam

# بارگیری داده‌ها
data = pd.read_csv('ETH-USD_hourly_data2.csv')
data['Datetime'] = pd.to_datetime(data['Datetime'])
data.set_index('Datetime', inplace=True)

# افزودن ویژگی‌های جدید (SMA, EMA)
data['SMA'] = data['Close'].rolling(window=5).mean()
data['EMA'] = data['Close'].ewm(span=5, adjust=False).mean()

# حذف سطرهای دارای مقدارهای NaN (به علت محاسبات اندیکاتورها)
data.dropna(inplace=True)

# استخراج ویژگی‌ها و نرمال‌سازی آنها
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data[['Close', 'SMA', 'EMA']])

# ایجاد مجموعه داده‌های آموزشی
def create_dataset(data, look_back=60):
    X, y = [], []
    for i in range(len(data) - look_back - 1):
        X.append(data[i:(i + look_back)])
        y.append(data[i + look_back, 0])
    return np.array(X), np.array(y)

look_back = 90
X, y = create_dataset(scaled_data, look_back)

# تقسیم داده‌ها به مجموعه‌های آموزشی و تست
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# تغییر شکل داده‌ها به فرم [samples, time steps, features]
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2])
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2])

from tensorflow.keras.models import load_model

model = load_model('my_model.h5')





# پیش‌بینی قیمت‌ها با استفاده از داده‌های تست
predictions = model.predict(X_test)

# بازگرداندن پیش‌بینی‌ها به مقیاس اصلی
predictions_extended = np.zeros((predictions.shape[0], 3))
predictions_extended[:, 0] = predictions.flatten()

predictions = scaler.inverse_transform(predictions_extended)[:, 0]

# بازگرداندن قیمت‌های واقعی به مقیاس اصلی
real_prices_extended = np.zeros((y_test.shape[0], 3))
real_prices_extended[:, 0] = y_test

real_prices = scaler.inverse_transform(real_prices_extended)[:, 0]

# رسم نمودار مقایسه پیش‌بینی‌ها با قیمت‌های واقعی
plt.figure(figsize=(14, 5))
plt.plot(real_prices, label='قیمت واقعی')
plt.plot(predictions, label='قیمت پیش‌بینی شده')
plt.title('پیش‌بینی قیمت ارز')
plt.xlabel('روز')
plt.ylabel('قیمت')
plt.legend()
plt.show()

# انتخاب آخرین داده‌ها برای پیش‌بینی 5 روز آینده
last_days = scaled_data[-look_back:]
predicted_prices = []
tedadRooz = 5

for _ in range(tedadRooz):
    # پیش‌بینی قیمت روز بعد
    prediction = model.predict(last_days.reshape(1, look_back, X_train.shape[2]))
    predicted_prices.append(prediction[0, 0])

    # افزودن پیش‌بینی به داده‌ها به عنوان داده واقعی
    new_row = np.zeros((1, 3))
    new_row[0, 0] = prediction
    new_row[0, 1] = last_days[-1, 1]  # استفاده از آخرین SMA واقعی
    new_row[0, 2] = last_days[-1, 2]  # استفاده از آخرین EMA واقعی
    
    last_days = np.vstack([last_days[1:], new_row])
    
    # بازآموزی مدل با داده‌های جدید برای بهبود دقت پیش‌بینی
    X_train_new = np.vstack([X_train, last_days.reshape(1, look_back, X_train.shape[2])])
    y_train_new = np.append(y_train, prediction[0, 0])
    
    model.fit(X_train_new, y_train_new, batch_size=16, epochs=10, verbose=0)

# بازگرداندن مقادیر به مقیاس اصلی
predicted_prices_extended = np.zeros((tedadRooz, 3))
predicted_prices_extended[:, 0] = np.array(predicted_prices).flatten()

predicted_prices = scaler.inverse_transform(predicted_prices_extended)[:, 0]
print(f'پیش‌بینی قیمت 5 روز آینده: {predicted_prices}')
for i in range(1, tedadRooz+1):
    print(f'{i} forecast: {predicted_prices[i-1:i]}')

# محاسبه دقت مدل با استفاده از RMSE
from sklearn.metrics import mean_squared_error
rmse = np.sqrt(mean_squared_error(real_prices, predictions))
print(f'RMSE: {rmse}')

# رسم نمودار ترکیبی 15 روز آخر واقعی + 5 روز پیش‌بینی‌شده
real_prices_last_15_days = real_prices[-15:]

# ایجاد آرایه جدید برای نگهداری داده‌های ترکیبی (15 روز واقعی + 5 روز پیش‌بینی‌شده)
combined_prices = np.concatenate([real_prices_last_15_days, predicted_prices])

# ایجاد برچسب‌های زمانی برای نمودار
days = np.arange(1, len(combined_prices) + 1)

real_prices2 = np.array(real_prices[-10:])
predictions2 = np.array(list(predictions[-10:]) + list(predicted_prices))
plt.plot(real_prices2, color='blue')
plt.plot(predictions2, color='red')
plt.show()


