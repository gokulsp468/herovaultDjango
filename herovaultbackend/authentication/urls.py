
from django.urls import path
from . import views
from rest_framework_simplejwt.views import  TokenRefreshView
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('signUp/', views.SignUpView, name='signUp'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
