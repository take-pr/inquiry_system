from django.contrib.auth import views as auth_views
from django.urls import path
from .views import (
    home_view, inquiry_view, success_view, task_list, task_create, task_edit, task_delete, 
    task_update_status, task_status_data, task_detail, task_progress_chart, 
    server_monitor_view, get_system_stats, user_register, custom_logout_view
)

urlpatterns = [
    path('', home_view, name='home'),  # ホーム画面のURL
    path('inquiry/', inquiry_view, name='inquiry'),
    path('success/', success_view, name='success'),
    path('tasks/', task_list, name='task_list'),
    path('tasks/<int:pk>/', task_detail, name='task_detail'),
    path('tasks/create/', task_create, name='task_create'),
    path('tasks/edit/<int:pk>/', task_edit, name='task_edit'),
    path('tasks/delete/<int:pk>/', task_delete, name='task_delete'),
    path('tasks/status/<int:pk>/<str:status>/', task_update_status, name='task_update_status'),
    path('tasks/status-data/', task_status_data, name='task_status_data'),
    path('tasks/progress-chart/', task_progress_chart, name='task_progress_chart'),
    path('server-monitor/', server_monitor_view, name='server_monitor'),
    path('get-system-stats/', get_system_stats, name='get_system_stats'),
    path('register/', user_register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', custom_logout_view, name='logout'), 
]