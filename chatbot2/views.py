# chatbot2/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# بارگذاری مدل فارسی
model_name = "HooshvareLab/bert-fa-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
chatbot = pipeline('text-generation', model=model, tokenizer=tokenizer)

class ChatBotAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_message = request.data.get('message')
        bot_response = chatbot(user_message, max_length=50)[0]['generated_text']

        # ذخیره پیام و پاسخ در پایگاه داده (اختیاری)
        # ChatMessage.objects.create(
        #     user_message=user_message,
        #     bot_response=bot_response
        # )

        return Response({'response': bot_response}, status=status.HTTP_200_OK)


from django.shortcuts import render

def chat_view(request):
    return render(request, 'chat2.html')
