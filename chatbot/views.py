from django.shortcuts import render
from .models import ChatMessage, User, Symptom, Disease, ChatSession
from openai import OpenAI
from medical_chatbot import settings

apikey = settings.OPENAI_API_KEY
client = OpenAI(api_key=apikey)

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

def chatbot_view(request):
    user = get_or_create_default_user()
    bot_response = None

    # مدیریت جلسات چت
    session_id = request.session.get('chat_session_id')
    if not session_id:
        session = ChatSession.objects.create(user=user)
        request.session['chat_session_id'] = session.id
    else:
        session = ChatSession.objects.get(id=session_id)

    if request.method == 'POST':
        user_message = request.POST.get('message')

        # ذخیره پیام کاربر
        ChatMessage.objects.create(session=session, user=user, message=user_message, is_bot=False)

        # جستجوی اطلاعات پزشکی
        medical_info = get_medical_info(user_message)
        if medical_info:
            bot_message = medical_info
        else:
            # تولید پاسخ از GPT
            past_messages = generate_chat_context(session)
            past_messages.insert(0, {"role": "system", "content": "شما یک پزشک بسیار دانا و با تجربه هستید. وظیفه شما تشخیص بیماری‌ها و پیشنهاد درمان‌های مناسب است. علائم بیمار را با دقت بررسی کنید و پیشنهادهای درمانی بدهید."})

            response = client.chat.completions.create(
                messages=past_messages + [{"role": "user", "content": user_message}],
                model="gpt-4o-mini",
                temperature= 0.7,
                max_tokens=200,
            )
            bot_message = response.choices[0].message.content

        # ذخیره پیام بات
        ChatMessage.objects.create(session=session, user=user, message=bot_message, is_bot=True)

        # ارسال پاسخ به قالب HTML
        bot_response = bot_message

    return render(request, 'chat.html', {'bot_response': bot_response})
