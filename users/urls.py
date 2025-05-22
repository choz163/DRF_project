from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, RegisterView, PaymentViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]
