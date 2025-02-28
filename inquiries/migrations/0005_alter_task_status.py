# Generated by Django 5.1.6 on 2025-02-16 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiries', '0004_task_deadline_task_priority_alter_task_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('not_started', '未着手'), ('in_progress', '進行中'), ('done', '完了')], default='not_started', max_length=15, verbose_name='ステータス'),
        ),
    ]
