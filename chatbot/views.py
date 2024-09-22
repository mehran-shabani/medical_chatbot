from rest_framework.response import Response
from rest_framework import status
from .models import ChatMessage, ChatSession
from .cleaner import clean_bot_message
from .generateresponse import (
    get_or_create_default_user, 
    get_medical_info, 
    generate_gpt_response, 
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatMessage, ChatSession
from .cleaner import clean_bot_message
from .generateresponse import (
    get_or_create_default_user, 
    get_medical_info, 
    generate_gpt_response, 
)
from .serializers import ChatMessageSerializer  # اطمینان حاصل کنید که این خط درست است

class ChatbotAPIView(APIView):
    def post(self, request):
        serializer = ChatMessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # دریافت یا ایجاد کاربر پیش‌فرض
        user = get_or_create_default_user()

        # مدیریت جلسات چت
        session_id = request.session.get('chat_session_id')
        if not session_id:
            session = ChatSession.objects.create(user=user)
            request.session['chat_session_id'] = session.id
        else:
            session = ChatSession.objects.get(id=session_id)

        user_message = serializer.validated_data['message']

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

        return Response({"bot_response": bot_message}, status=status.HTTP_200_OK)

