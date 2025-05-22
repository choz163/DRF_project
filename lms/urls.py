from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, SubscriptionAPIView

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='course')
router.register('lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    *router.urls,
    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscription'),
]
