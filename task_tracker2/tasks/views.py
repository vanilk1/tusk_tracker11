from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CommentForm, RegisterForm, TaskFilterForm, TaskForm
from .models import Comment, Task
from .permissions import OwnerRequiredMixin


# ---------------------------------------------------------------------------
# Реєстрація користувача
# ---------------------------------------------------------------------------

class RegisterView(CreateView):
    """Реєстрація нового користувача (автоматичний вхід після реєстрації)."""

    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f'Ласкаво просимо, {self.object.username}!')
        return response


# ---------------------------------------------------------------------------
# Список завдань + фільтрація
# ---------------------------------------------------------------------------

class TaskListView(LoginRequiredMixin, ListView):
    """
    Список завдань поточного користувача з фільтрацією
    за статусом, пріоритетом, терміном виконання та пошуком за назвою.
    """

    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.filter(owner=self.request.user)

        self.filter_form = TaskFilterForm(self.request.GET or None)
        if self.filter_form.is_valid():
            status = self.filter_form.cleaned_data.get('status')
            priority = self.filter_form.cleaned_data.get('priority')
            due_date = self.filter_form.cleaned_data.get('due_date')
            query = self.filter_form.cleaned_data.get('q')

            if status:
                queryset = queryset.filter(status=status)
            if priority:
                queryset = queryset.filter(priority=priority)
            if due_date:
                queryset = queryset.filter(due_date=due_date)
            if query:
                queryset = queryset.filter(title__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form

        all_tasks = Task.objects.filter(owner=self.request.user)
        context['stats'] = {
            'total': all_tasks.count(),
            'todo': all_tasks.filter(status=Task.Status.TODO).count(),
            'in_progress': all_tasks.filter(status=Task.Status.IN_PROGRESS).count(),
            'done': all_tasks.filter(status=Task.Status.DONE).count(),
            'overdue': sum(1 for t in all_tasks if t.is_overdue),
        }
        return context


# ---------------------------------------------------------------------------
# Деталі завдання + коментарі
# ---------------------------------------------------------------------------

class TaskDetailView(LoginRequiredMixin, DetailView):
    """Детальна сторінка завдання зі списком коментарів і формою додавання коментаря."""

    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('author')
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        """Обробка додавання нового коментаря."""
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, 'Коментар додано.')
            return redirect('task_detail', pk=self.object.pk)

        context = self.get_context_data(comment_form=form)
        return self.render_to_response(context)


# ---------------------------------------------------------------------------
# Створення / редагування / видалення завдання
# ---------------------------------------------------------------------------

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Завдання створено.')
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Завдання оновлено.')
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        messages.success(self.request, 'Завдання видалено.')
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Видалення коментаря (лише автор коментаря або власник завдання)
# ---------------------------------------------------------------------------

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_queryset(self):
        # Видалити коментар може лише його автор або власник завдання
        return Comment.objects.filter(author=self.request.user) | Comment.objects.filter(
            task__owner=self.request.user
        )

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.task.pk})
