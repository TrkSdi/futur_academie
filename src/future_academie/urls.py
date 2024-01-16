from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views


from private_app.views import LogoutAPIView, LogoutAPIView2, activate_user

urlpatterns = [
    # Honeypot fake admin login
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("admin_future/", admin.site.urls),
    path("API_private/", include("private_app.urls")),
    path("API_public/", include("public_app.urls")),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('logout2/', LogoutAPIView2.as_view(), name='logout'),
    path('activate/<str:uid>/<str:token>/',
         activate_user, name='activate'),


]
