import psutil  # サーバーリソースを取得するためのライブラリ
from django.contrib.auth.decorators import login_required  # ログイン必須にする
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Count, Case, When, IntegerField
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator  # ページネーション機能を追加
from django.conf import settings
from django.contrib.auth import login, logout
from .models import Task
from .forms import InquiryForm, TaskForm, UserRegisterForm

# ホーム画面
def home_view(request):
    return render(request, 'home.html')

# 問い合わせフォームの表示・送信処理
def inquiry_view(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = InquiryForm()
    return render(request, 'inquiries/inquiry_form.html', {'form': form})

# 問い合わせ送信成功画面
def success_view(request):
    return render(request, 'inquiries/success.html')

# タスク一覧の表示（検索・フィルタ・ソート・ページネーション対応）
@login_required
def task_list(request):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'deadline')
    filter_status = request.GET.get('status', 'all')
    page_number = request.GET.get('page', 1)  # 現在のページ番号を取得（デフォルトは1）

    # ログインユーザーのタスクのみ取得
    tasks = Task.objects.filter(user=request.user)

    # 検索機能
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    # ステータスでフィルタリング
    if filter_status in ['done', 'in_progress', 'not_started']:
        tasks = tasks.filter(status=filter_status)

    # ソート機能（優先度順を逆にする）
    if sort_by == 'priority':
        tasks = tasks.order_by('priority')  # 優先度の高いものが上に
    elif sort_by == 'deadline':
        tasks = tasks.order_by('deadline')

    # ページネーション設定（1ページ5件表示）
    paginator = Paginator(tasks, 5)
    tasks_page = paginator.get_page(page_number)

    # 進捗率計算（完了したタスクの割合）
    total_tasks = tasks.count()
    done_tasks = tasks.filter(status='done').count()
    progress_rate = (done_tasks / total_tasks * 100) if total_tasks > 0 else 0

    # 締め切りが近いタスクの判定
    today = timezone.now().date()
    for task in tasks_page:
        task.is_urgent = task.deadline and (task.deadline - today).days <= 3

    return render(request, 'inquiries/task_list.html', {
        'tasks': tasks_page,  # ページネーション適用後のタスクリスト
        'paginator': paginator,  # ページネーション情報を渡す
        'progress_rate': progress_rate,
        'search_query': search_query,
        'sort_by': sort_by,
        'filter_status': filter_status,
    })

# タスクの詳細画面
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'inquiries/task_detail.html', {'task': task})

# 新規タスクの作成
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'inquiries/task_form.html', {'form': form})

# 既存タスクの編集
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'inquiries/task_form.html', {'form': form})

# タスクの削除
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'inquiries/task_confirm_delete.html', {'task': task})

# タスクのステータス更新（進行中・完了など）
def task_update_status(request, pk, status):
    task = get_object_or_404(Task, pk=pk)

    # ステータスが正しいかチェック
    valid_statuses = [choice[0] for choice in Task.STATUS_CHOICES]
    if status in valid_statuses:
        task.status = status
        task.save()

    return redirect('task_list')

# 進捗状況のデータ取得（棒グラフ用）
def task_status_data(request):
    task_counts = {
        '未着手': Task.objects.filter(status='not_started').count(),
        '進行中': Task.objects.filter(status='in_progress').count(),
        '完了': Task.objects.filter(status='done').count(),
    }
    return JsonResponse(task_counts)

# 進捗状況のグラフデータ取得（JSON形式）
def task_progress_chart(request):
    progress_data = Task.objects.values('status').annotate(count=Count('status'))
    return JsonResponse(list(progress_data), safe=False)


# サーバー監視ページの表示
def server_monitor_view(request):
    return render(request, 'monitor/server_monitor.html')

# CPU・メモリの使用率を取得
def get_system_stats(request):
    # CPU & メモリ使用率
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    # ディスク使用率
    disk_info = get_disk_usage()

    # ネットワーク使用量
    network_info = get_network_usage()

    # プロセス一覧（上位5つのプロセスを取得）
    processes = get_running_processes()[:5]

    # エラーログ
    error_logs = get_error_logs()

    return JsonResponse({
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_total': disk_info['total'],
        'disk_used': disk_info['used'],
        'disk_free': disk_info['free'],
        'disk_percent': disk_info['percent'],
        'bytes_sent': network_info['bytes_sent'],
        'bytes_recv': network_info['bytes_recv'],
        'processes': processes,
        'error_logs': error_logs
    })



# ディスク使用率の取得
def get_disk_usage():
    disk = psutil.disk_usage('/')
    return {
        'total': disk.total // (1024 ** 3),  # GB単位
        'used': disk.used // (1024 ** 3),
        'free': disk.free // (1024 ** 3),
        'percent': disk.percent  # 使用率
    }


# ネットワーク監視（送受信データ量）
def get_network_usage():
    net = psutil.net_io_counters()
    return {
        'bytes_sent': net.bytes_sent // (1024 ** 2),  # MB単位
        'bytes_recv': net.bytes_recv // (1024 ** 2)
    }


# プロセス監視
def get_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append(proc.info)
    return processes


# エラーログ監視（Djangoログの異常検知）
import os

LOG_FILE_PATH = "logs/error.log"

def get_error_logs():
    if not os.path.exists(LOG_FILE_PATH):
        return "ログファイルが見つかりません。"

    with open(LOG_FILE_PATH, "r", encoding="utf-8") as log_file:
        logs = log_file.readlines()[-10:]  # 最新の10行を取得
    return "".join(logs)


# 障害通知（メールでアラート送信）
def send_alert_email(subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ['admin@example.com'],  # 送信先（必要に応じて変更）
        fail_silently=False,
    )

def check_system_health():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = get_disk_usage()['percent']

    if cpu > 90 or memory > 90 or disk > 90:
        subject = "⚠️ サーバー負荷警告！"
        message = f"CPU: {cpu}%, メモリ: {memory}%, ディスク: {disk}%"
        send_alert_email(subject, message)


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 登録後すぐにログイン
            return redirect('home')  # 登録後、ホームへリダイレクト
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})


# ログアウト処理（Django標準のLogoutViewではなく、自前で作成）
def custom_logout_view(request):
    logout(request)  # ログアウト処理
    return render(request, 'users/logout_success.html')  # ログアウト完了ページを表示