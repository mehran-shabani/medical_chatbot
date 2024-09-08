from django.shortcuts import render
from .forms import ChatForm
from .models import ChatMessage, User
from openai import OpenAI
from medical_chatbot import settings

apikey = settings.OPENAI_API_KEY
client = OpenAI(api_key=apikey)

def get_or_create_default_user():
    # این تابع یک کاربر پیش‌فرض را در پایگاه داده ایجاد می‌کند (در صورتی که وجود نداشته باشد)
    user, created = User.objects.get_or_create(
        name="کاربر فرضی", 
        defaults={"phone_number": "0000000000", "email": "default@example.com"}
    )
    return user

def chatbot_view(request):
    user = get_or_create_default_user()  # دریافت کاربر پیش‌فرض
    bot_response = None

    if request.method == 'POST':
        user_message = request.POST.get('message')  # دریافت پیام از فرم

        # ذخیره پیام کاربر
        ChatMessage.objects.create(user=user, message=user_message, is_bot=False)

        # تولید پاسخ از GPT
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an experienced medical doctor."},
                {"role": "user", "content": user_message},
            ],
            model="gpt-4",
        )

        # دریافت پاسخ
        bot_message = response.choices[0].message.content

        # ذخیره پیام بات
        ChatMessage.objects.create(user=user, message=bot_message, is_bot=True)

        # ارسال پاسخ به قالب HTML
        bot_response = bot_message

    return render(request, 'chat.html', {'bot_response': bot_response})
