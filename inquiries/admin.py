from django.contrib import admin
from .models import Inquiry, Task

# Inquiryモデルを管理画面に登録
@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')  # 一覧に表示する項目
    search_fields = ('name', 'email')  # 検索機能
    list_filter = ('created_at',)  # フィルター機能


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at', 'updated_at')  # 一覧に表示する項目
    list_filter = ('status',)  # ステータスでフィルタリング
    search_fields = ('title', 'description')  # 検索機能
