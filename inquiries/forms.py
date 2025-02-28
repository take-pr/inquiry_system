from django import forms
from .models import Inquiry, Task  # Task もインポート
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'message']  # 問い合わせ用フォーム

# TaskForm を追加
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'deadline']  # 優先度・締め切りを追加
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="有効なメールアドレスを入力してください。")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']