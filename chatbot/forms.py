# chatbot/forms.py
from django import forms

class ChatForm(forms.Form):
    message = forms.CharField(
        label='پیام شما',
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 50}),
        max_length=1000
    )
