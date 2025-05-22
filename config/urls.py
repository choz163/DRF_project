from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lms.views import CourseViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
  path('admin/', admin.site.urls),
  path('api/', include('lms.urls')),
  path('', include('users.urls')),
  path('api/', include(router.urls)),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
