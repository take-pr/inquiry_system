# Generated by Django 5.1.6 on 2025-02-14 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('not_started', '未着手'), ('in_progress', '進行中'), ('completed', '完了')], default='not_started', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
