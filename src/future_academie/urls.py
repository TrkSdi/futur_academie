from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from private_app.views import LogoutAPIView, ActivateUser

urlpatterns = [
    # Honeypot fake admin login
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("admin_future/", admin.site.urls),
    path("API_private/", include("private_app.urls")),
    path("API_public/", include("public_app.urls")),


    # account user part

    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),

    path('accounts/activate/<uid>/<token>',
         ActivateUser.as_view({'get': 'activation'}), name='activation'),

    # to obtain (POST) refresh and access token
    path('auth/jwt/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),

]
