from transformers import AutoModelForCausalLM, AutoTokenizer

# نام مدل را مشخص کنید
model_name = 'microsoft/DialoGPT-mini'

# بارگذاری مدل و توکنایزر
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# مسیر دایرکتوری محلی برای ذخیره مدل
local_model_path = 'models'

# ذخیره مدل و توکنایزر در دایرکتوری محلی
model.save_pretrained(local_model_path)
tokenizer.save_pretrained(local_model_path)




from transformers import pipeline

# مسیر دایرکتوری محلی که مدل در آن ذخیره شده است
local_model_path = 'models'

# بارگذاری مدل و توکنایزر از دایرکتوری محلی
chatbot = pipeline('text-generation', model=local_model_path, tokenizer=local_model_path)

# تابع برای ارسال پیام و دریافت پاسخ
def get_bot_response(user_message):
    response = chatbot(user_message, max_length=100, num_return_sequences=1)
    return response[0]['generated_text']

# تست تابع با ورودی‌های مختلف
user_messages = [
    "سلام",
    "چه خبرا؟",
    "آیار اوضاع بر وفق مراد هست؟"
]

for msg in user_messages:
    print(f"پیام: {msg}")
    print(f"پاسخ: {get_bot_response(msg)}")
    print("-" * 50)
