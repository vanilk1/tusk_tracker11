from django.conf import settings
from django.db import models
from django.urls import reverse


class Task(models.Model):
    """Завдання користувача."""

    class Status(models.TextChoices):
        TODO = 'todo', 'До виконання'
        IN_PROGRESS = 'in_progress', 'В процесі'
        DONE = 'done', 'Виконано'

    class Priority(models.TextChoices):
        LOW = 'low', 'Низький'
        MEDIUM = 'medium', 'Середній'
        HIGH = 'high', 'Високий'

    title = models.CharField('Назва', max_length=200)
    description = models.TextField('Опис', blank=True)
    status = models.CharField(
        'Статус', max_length=20, choices=Status.choices, default=Status.TODO
    )
    priority = models.CharField(
        'Пріоритет', max_length=20, choices=Priority.choices, default=Priority.MEDIUM
    )
    due_date = models.DateField('Термін виконання', null=True, blank=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Власник',
    )

    created_at = models.DateTimeField('Створено', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Завдання'
        verbose_name_plural = 'Завдання'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'pk': self.pk})

    @property
    def is_overdue(self):
        from django.utils import timezone
        return bool(
            self.due_date
            and self.status != self.Status.DONE
            and self.due_date < timezone.localdate()
        )


class Comment(models.Model):
    """Коментар до завдання."""

    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments', verbose_name='Завдання'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField('Текст коментаря')
    created_at = models.DateTimeField('Створено', auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'

    def __str__(self):
        return f'Коментар від {self.author} до "{self.task}"'
