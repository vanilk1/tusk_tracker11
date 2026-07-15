from django.contrib.auth.mixins import UserPassesTestMixin


class OwnerRequiredMixin(UserPassesTestMixin):
    """
    Дозволяє доступ до вьюхи лише власнику об'єкта (Task.owner)
    або суперкористувачу/персоналу.

    Реалізує вимогу ТЗ: "система дозволів для обмеження доступу
    до редагування та видалення завдань".
    """

    raise_exception = False  # редіректить на 403-сторінку/логін замість помилки

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return user.is_authenticated and (obj.owner_id == user.id or user.is_staff)

    def handle_no_permission(self):
        from django.contrib import messages
        from django.shortcuts import redirect

        messages.error(self.request, 'У вас немає прав для виконання цієї дії.')
        return redirect('task_detail', pk=self.kwargs.get('pk'))
