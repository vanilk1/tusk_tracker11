from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Встроенные вьюхи Django для логина/логаута/смены пароля и т.д.
    # (используют шаблоны tasks/templates/registration/*.html)
    path('accounts/', include('django.contrib.auth.urls')),

    # Наше приложение
    path('', include('tasks.urls')),
]
