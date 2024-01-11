from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Honeypot fake admin login
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("admin_future/", admin.site.urls),
]
