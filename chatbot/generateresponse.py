import json
import requests
from .models import ChatMessage, Symptom, Disease, ChatSession, User
from medical_chatbot import settings

# دریافت کلید API از تنظیمات
apikey = settings.TALKBOT_API

def get_or_create_default_user():
    # ایجاد یا گرفتن کاربر پیش‌فرض
    user, created = User.objects.get_or_create(
        name="کاربر فرضی", 
        defaults={"phone_number": "0000000000", "email": "default@example.com"}
    )
    return user

def generate_chat_context(session):
    # تولید تاریخچه چت
    messages = []
    chat_messages = ChatMessage.objects.filter(session=session).order_by('created_at')
    for chat_message in chat_messages:
        role = "assistant" if chat_message.is_bot else "user"
        messages.append({"role": role, "content": chat_message.message})
    return messages

def get_medical_info(user_message):
    # جستجو در دیتابیس علائم و بیماری‌ها
    symptoms = Symptom.objects.filter(name__icontains=user_message)
    if symptoms.exists():
        diseases = Disease.objects.filter(symptoms__in=symptoms)
        if diseases.exists():
            return f"بر اساس علائم شما، ممکن است دچار {', '.join(d.name for d in diseases)} باشید."
    return None

def is_message_complete(message):
    # بررسی می‌کند که آیا پیام به نقطه پایانی منطقی رسیده است یا خیر.
    end_symbols = ['.', '!', '؟', '؟']  # علائم پایانی منطقی
    return any(message.strip().endswith(symbol) for symbol in end_symbols)

def remove_repeated_phrases(text):
    # این تابع جملات تکراری را از پاسخ حذف می‌کند.
    sentences = text.split('. ')
    seen = set()
    cleaned_sentences = []
    
    for sentence in sentences:
        if sentence not in seen:
            cleaned_sentences.append(sentence)
            seen.add(sentence)
    
    return '. '.join(cleaned_sentences)

def generate_gpt_response(session, user_message, max_history_length=1):
    # تولید پیام‌های گذشته (تاریخچه مکالمه)
    past_messages = generate_chat_context(session)
    
    # محدود کردن تعداد پیام‌های گذشته به max_history_length (فقط 5 پیام آخر)
    if len(past_messages) > max_history_length:
        past_messages = past_messages[-max_history_length:]  # فقط 5 پیام آخر

    # اضافه کردن پیام سیستمی برای تعیین نقش ربات
    past_messages.insert(0, {"role": "system", "content": "شما یک پزشک بسیار دانا و با تجربه هستید. وظیفه شما تشخیص بیماری‌ها و پیشنهاد درمان‌های مناسب است. علائم بیمار را با دقت بررسی کنید و پیشنهادهای درمانی بدهید."})

    # ارسال درخواست به API
    url = 'https://api.talkbot.ir/v1/chat/completions'
    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": past_messages + [{"role": "user", "content": user_message}],
        "max_token": 4000,
        "temperature": 0.3,
        "stream": False,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {apikey}'  # استفاده از کلید API
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.ok:
        # دریافت پاسخ اولیه
        bot_message = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
        
        # حذف جملات تکراری
        bot_message = remove_repeated_phrases(bot_message)

        # بررسی کامل بودن پاسخ
        while not is_message_complete(bot_message):
            additional_response = requests.post(url, data=json.dumps({
                "model": "gpt-4o",
                "messages": past_messages + [{"role": "user", "content": user_message}] + [{"role": "assistant", "content": bot_message}],
                "max_token": 50,
                "temperature": 0.7,
            }), headers=headers)
            
            if additional_response.ok:
                bot_message += " " + additional_response.json().get('choices', [{}])[0].get('message', {}).get('content', '')

        return bot_message
    else:
        return f'An error occurred: {response.text}'
