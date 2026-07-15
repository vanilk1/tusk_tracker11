import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Назва')),
                ('description', models.TextField(blank=True, verbose_name='Опис')),
                ('status', models.CharField(choices=[('todo', 'До виконання'), ('in_progress', 'В процесі'), ('done', 'Виконано')], default='todo', max_length=20, verbose_name='Статус')),
                ('priority', models.CharField(choices=[('low', 'Низький'), ('medium', 'Середній'), ('high', 'Високий')], default='medium', max_length=20, verbose_name='Пріоритет')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='Термін виконання')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Створено')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Оновлено')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL, verbose_name='Власник')),
            ],
            options={
                'verbose_name': 'Завдання',
                'verbose_name_plural': 'Завдання',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст коментаря')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Створено')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tasks.task', verbose_name='Завдання')),
            ],
            options={
                'verbose_name': 'Коментар',
                'verbose_name_plural': 'Коментарі',
                'ordering': ['created_at'],
            },
        ),
    ]
