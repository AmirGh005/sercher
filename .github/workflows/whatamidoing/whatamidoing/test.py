import yfinance as yf
import time

# تنظیمات برای دانلود داده‌ها
symbol = "ETH-USD"  # نماد ارز
start_date = "2024-09-10"  # تاریخ شروع
end_date = "2024-09-30"  # تاریخ پایان
filename = f"{symbol}_hourly_data2.csv"

# ایجاد یا به‌روزرسانی فایل CSV
while True:
    # دانلود داده‌های 5 دقیقه‌ای
    data = yf.download(symbol, start=start_date, end=end_date, interval="5m")

    # ذخیره داده‌های جدید به فایل CSV (جایگزینی فایل قبلی)
    data.to_csv(filename)

    print("داده‌ها با موفقیت به‌روزرسانی شدند.")

    # صبر کردن به مدت 5 دقیقه (300 ثانیه)
    time.sleep(300)
