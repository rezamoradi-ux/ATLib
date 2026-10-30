# ATLib — کتابخانه پیشرفته ربات تلگرام

**نسخه ۱.۰.۰** · API رسمی ربات تلگرام · ناهمزمان · مناسب تولید

ATLib یک فریم‌ورک ماژولار و ناهمزمان پایتون برای ساخت ربات‌های تلگرام با استفاده از **API رسمی ربات تلگرام** است. به سشن حساب کاربری یا کلاینت‌های غیررسمی وابسته نیست.

## ویژگی‌ها

- انتقال HTTP ناهمزمان با connection pooling، محدودیت نرخ و تلاش مجدد
- پردازش کامل به‌روزرسانی‌ها (long polling)
- سیستم Router / Handler با فیلترهای قابل ترکیب
- سازنده کیبورد اینلاین و ریپلای
- پشتیبانی از ایموجی سفارشی (Premium) با محاسبه صحیح آفست UTF-16
- پیام‌های غنی (Rich Messages – Bot API 10.1+)
- ماشین حالت محدود (FSM) با ذخیره‌سازی Memory و SQLite
- اعتبارسنجی HMAC برای `initData` مینی‌اپ
- پیکربندی تایپ‌شده، پنهان‌سازی توکن، لاگ ساختاریافته
- رابط خط فرمان (`atlib doctor`, `atlib init`)

## نصب

```bash
pip install atlib-telegram
```

## شروع سریع

```python
import os
from atlib import Application, Command

app = Application(token=os.environ["BOT_TOKEN"])

@app.router.message(Command("start"))
async def start(ctx):
    await ctx.answer("سلام از ATLib!")

if __name__ == "__main__":
    app.run_polling()
```

## مجوز

MIT
