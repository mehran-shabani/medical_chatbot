import os
import sys

# مسیر پروژه خود را به PYTHONPATH اضافه کنید
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

# تنظیمات Django را بارگذاری کنید
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_chatbot.settings')

import django
django.setup()

# حالا می‌توانید ماژول‌های Django را وارد کنید
from chatbot.models import ChatMessage, User

def count_user_messages(user_id):
    # پیدا کردن کاربر بر اساس user_id
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return f"کاربری با id {user_id} پیدا نشد."
    
    # شمارش تمام پیام‌های مربوط به این کاربر
    message_count = ChatMessage.objects.filter(user=user).count()

    return f"تعداد کل پیام‌ها برای کاربر با id {user_id}: {message_count}"

# نمونه فراخوانی تابع
print(count_user_messages(1))  # آی‌دی کاربر را تغییر دهید
