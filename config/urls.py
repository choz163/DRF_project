from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lms.urls')),        # всё lms сюда
    path('', include('users.urls')),      # ваши пользователи
]

