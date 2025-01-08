from pyrogram import Client, filters

# اطلاعات ضروری برای ورود به اکانت تلگرام
api_id = '24447677'
api_hash = 'b5b1aee85d98b5e14a66d990472bd09d'
phone_number = '+989362482673'

# نام فایل session برای ذخیره اطلاعات ورود
session_name = 'my_session'

# لیست کلمات کلیدی که باید بررسی شوند
keywords = [
    'machine learning', 'deep learning', 'regression', 'درخت تصمیم', 'ماشین لرنینگ',
    'یادگیری ماشین', 'data science', 'عصبی', 'یادگیری عمیق', 'هوش مصنوعی',
    'تحلیل داده', 'علوم کامپیوتر', 'علوم داده', 'Machine learning',
    'Deep learning', 'Regression', 'Data science', 'دیپ لرنینگ',
    'تحلیلگر','پایتون','برنامه نویس','آنالیز داده','لرنینگ','زبان R','مهندس کامپیوتر',
    'کامپیوتر','زبان طبیعی','nlp','NLP','بینایی ماشین','یادگیری تقویتی','vision',
    'reinforcement','Reinforcement','الگوریتم','پردازش تصویر','تحلیلگر دیتا','دانشجو شریف'
]  # لیستی از کلمات کلیدی

# آی‌دی تلگرامی که باید پیام‌ها به آن ارسال شود
target_id = '@Amir_GH_0505'

# ساخت و ورود به حساب تلگرام
app = Client(session_name, api_id=api_id, api_hash=api_hash, phone_number=phone_number)


# مانیتور کردن پیام‌های دریافتی
@app.on_message(filters.text)
def monitor_messages(client, message):
    # بررسی اگر هر کدام از کلمات لیست در پیام وجود داشته باشد
    if any(keyword in message.text for keyword in keywords):
        print(f"پیام پیدا شد: {message.text}")

        # فوروارد کردن پیام به آی‌دی دیگر
        client.forward_messages(target_id, message.chat.id, message.id)


# شروع مانیتورینگ
app.run()


