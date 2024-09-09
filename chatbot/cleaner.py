import re

# تابع تمیزکاری پیام
def clean_bot_message(message):
    # 1. حذف فاصله‌های اضافی از ابتدا و انتهای پیام
    cleaned_message = message.strip()
    
    # 2. حذف فاصله‌های دوبل داخل متن
    cleaned_message = re.sub(r'\s+', ' ', cleaned_message)  # تبدیل چند فاصله به یک فاصله
    
    # 3. تبدیل خط‌های جدید به <br> برای نمایش در HTML
    cleaned_message = cleaned_message.replace('\n', '<br>')
    
    # 4. اصلاح علائم نگارشی در زبان فارسی
    # جایگزینی ویرگول انگلیسی با فارسی
    cleaned_message = cleaned_message.replace(',', '،')
    
    # اصلاح نقاط دوبل یا بیشتر
    cleaned_message = re.sub(r'\.{2,}', '…', cleaned_message)  # تبدیل چند نقطه به …
    
    # 5. اصلاح نیم‌فاصله‌ها
    # تبدیل فاصله‌های نیم‌فاصله ناقص به نیم‌فاصله صحیح
    cleaned_message = re.sub(r'\s*-\s*', '‌', cleaned_message)  # استفاده از نیم‌فاصله صحیح

    # حذف فاصله‌های قبل و بعد از خط تیره (برای حالت‌های خاص که ممکن است اشتباه وارد شده باشند)
    cleaned_message = re.sub(r'\s*-\s*', '-', cleaned_message)

    # 6. جایگزینی کاراکترهای خاص
    cleaned_message = cleaned_message.replace('!', '!')
    
    # 7. حذف کاراکترهای غیرمجاز یا غیرضروری
    cleaned_message = re.sub(r'[^\w\s\.\،\؟\!\-\«\»\"\(\)\[\]\{\}]', '', cleaned_message)

    # 8. اصلاح فاصله‌گذاری علائم نگارشی
    cleaned_message = re.sub(r'\s*([،.؟!…])', r'\1', cleaned_message)  # حذف فاصله قبل از علائم
    cleaned_message = re.sub(r'([،.؟!…])\s*', r'\1 ', cleaned_message)  # افزودن فاصله بعد از علائم
    
    # 9. تبدیل نقل‌قول‌ها به شکل استاندارد
    cleaned_message = cleaned_message.replace('"', '«').replace("'", "»")
    
    # 10. جایگزینی پرانتزهای انگلیسی با فارسی
    cleaned_message = cleaned_message.replace('(', '«').replace(')', '»')

    # 11. حذف تکرار کلمات یا علائم نگارشی
    cleaned_message = re.sub(r'(.)\1{2,}', r'\1\1', cleaned_message)  # بیش از دو تکرار کاراکتر را به دو تا کاهش می‌دهد
    
    # 12. اصلاح نمایش اعداد و حروف لاتین
    cleaned_message = re.sub(r'(\d)([^\d\s])', r'\1 \2', cleaned_message)  # عدد چسبیده به حرف
    cleaned_message = re.sub(r'([^\d\s])(\d)', r'\1 \2', cleaned_message)  # حرف چسبیده به عدد

    # 13. اصلاح جمع‌های بدون نیم‌فاصله (مثل "مسکنها" -> "مسکن‌ها")
    cleaned_message = re.sub(r'(\b\w+?)(ها)(\s|$)', r'\1‌ها\3', cleaned_message)

    return cleaned_message

