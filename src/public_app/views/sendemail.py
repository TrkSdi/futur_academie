# Third-party imports
import environ
import os
from rest_framework import viewsets
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework.decorators import action
from rest_framework import permissions
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# env is an instance of environ
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


class SendEmailViewSetPublic(viewsets.ViewSet):

    # permission
    permission_classes = [permissions.AllowAny]

    @csrf_exempt
    @action(detail=False, methods=["POST"])
    def send_email_view(self, request):
        # recovery json file
        data = json.loads(request.body.decode("utf-8"))
        # recovery json keys
        textEmail = data.get("textEmail")
        subject = data.get("subject")
        recipient = data.get("recipient")

        # function send email
        send_mail(
            subject,
            textEmail,
            recipient,
            [env.str("EMAIL_HOST_USER")],
            fail_silently=False,
            auth_user=None,
            auth_password=None,
            connection=None,
            html_message=None,
        )
        # send email waits an answer
        return Response(status=status.HTTP_200_OK)
