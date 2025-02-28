from django.db import models
from django.contrib.auth.models import User  # Djangoのユーザーモデルをインポート

class Inquiry(models.Model):
    name = models.CharField(max_length=100)  # 名前
    email = models.EmailField()  # メールアドレス
    message = models.TextField()  # メッセージ内容
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時（自動で現在日時が追加される）

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
    ]
    
    STATUS_CHOICES = [
        ('not_started', '未着手'),
        ('in_progress', '進行中'),
        ('done', '完了'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # ✅ 既存データのために null=True を追加
    title = models.CharField(max_length=200, verbose_name="タイトル")
    description = models.TextField(blank=True, verbose_name="詳細")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="優先度")
    deadline = models.DateField(null=True, blank=True, verbose_name="締め切り")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_started', verbose_name="ステータス")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")
    is_completed = models.BooleanField(default=False) # いる？

    def __str__(self):
        return f"{self.title}（{self.user.username}）"