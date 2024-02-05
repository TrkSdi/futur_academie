from django.http import HttpResponse
from djoser.utils import decode_uid
from djoser.conf import settings as djoser_settings
from rest_framework import status
from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect
from private_app.models import User

from djoser.views import UserViewSet
from rest_framework.response import Response


class ActivateUser(UserViewSet):
    permission_classes = [AllowAny]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())

        kwargs["data"] = {"uid": self.kwargs["uid"], "token": self.kwargs["token"]}

        return serializer_class(*args, **kwargs)

    def activation(self, request, *args, **kwargs):
        response = super().activation(request, *args, **kwargs)

        if response.status_code == status.HTTP_204_NO_CONTENT:
            return redirect("http://localhost:4200/login")
        return response
