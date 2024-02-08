# Third-party imports
from rest_framework import viewsets
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json


class SendEmailViewSetPublic(viewsets.ViewSet):

    @csrf_exempt
    def send_email_view(request):
        data = json.loads(request.body.decode("utf-8"))
        textEmail = data.get("textEmail")
        subject = data.get("subject")
        recipient = data.get("recipient")
        print(
            f"data : {data}\n, texte : {textEmail}\n, sujet : {subject}\n, expediteur : {recipient}"
        )

        # Envoyer l'email
        send_mail(
            subject,
            textEmail,
            recipient,
            ["damienvialla@yahoo.fr"],
            fail_silently=False,
            auth_user=None,
            auth_password=None,
            connection=None,
            html_message=None,
        )
