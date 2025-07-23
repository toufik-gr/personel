from django import forms
from django.contrib.auth.forms import AuthenticationForm

class ArabicAuthentForm(AuthenticationForm):
    
    username = forms.CharField(
        label="",  # Arabic label for Username
        widget=forms.TextInput(attrs={
            'class': 'form-control text-right',
            'placeholder': 'اسم المستخدم'
        })
    )
    password = forms.CharField(
        label="",  # Arabic label for Password
        widget=forms.PasswordInput(attrs={
            'class': 'form-control text-right',
            'placeholder': 'كلمة المرور'
        })
    )
