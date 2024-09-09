# chabot/views.py
from django.shortcuts import render
from .models import ChatMessage, ChatSession
from openai import OpenAI
from medical_chatbot import settings
from .cleaner import clean_bot_message


apikey = settings.OPENAI_API_KEY
client = OpenAI(api_key=apikey)

from django.shortcuts import render
from .generateresponse import (
    get_or_create_default_user, 
    get_medical_info, 
    generate_gpt_response, 
    
)
from .models import ChatMessage, ChatSession

def chatbot_view(request):
    # دریافت یا ایجاد کاربر پیش‌فرض
    user = get_or_create_default_user()

    # مدیریت جلسات چت
    session_id = request.session.get('chat_session_id')
    if not session_id:
        session = ChatSession.objects.create(user=user)
        request.session['chat_session_id'] = session.id
    else:
        session = ChatSession.objects.get(id=session_id)

    bot_response = None
    if request.method == 'POST':
        user_message = request.POST.get('message')

        # ذخیره پیام کاربر
        ChatMessage.objects.create(session=session, user=user, message=user_message, is_bot=False)

        # بررسی اطلاعات پزشکی
        medical_info = get_medical_info(user_message)
        if medical_info:
            bot_message = medical_info
        else:
            # تولید پاسخ از GPT
            bot_message = generate_gpt_response(session, user_message)

        # تمیز کردن پیام بات
        bot_message = clean_bot_message(bot_message)

        # ذخیره پیام بات
        ChatMessage.objects.create(session=session, user=user, message=bot_message, is_bot=True)

        # ارسال پاسخ به قالب HTML
        bot_response = clean_bot_message(bot_message)

    return render(request, 'chat.html', {'bot_response': bot_response})
