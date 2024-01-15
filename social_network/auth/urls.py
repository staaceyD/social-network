from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from social_network.auth.views import register_user, user_activity_view

urlpatterns = [
    path("register", register_user, name="register"),
    path("login", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("activity", user_activity_view, name="activity"),
]
