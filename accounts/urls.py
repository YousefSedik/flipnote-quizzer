from django.urls import path
from rest_framework_simplejwt.views import (
    token_obtain_pair,
    token_refresh,
    token_verify,
)
from .api import create_user, view_profile

app_name = "accounts"
urlpatterns = [
    path("login/", token_obtain_pair, name="token_obtain_pair"),
    path("token/refresh/", token_refresh, name="token_refresh"),
    path("token/verify/", token_verify, name="token_verify"),
    path("register/", create_user, name="create_user"),
    path("profile/", view_profile, name="view_profile"),
]
