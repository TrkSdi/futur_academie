from django.contrib.auth import get_user_model
from django.http import HttpResponse
from djoser.utils import decode_uid
from djoser.conf import settings as djoser_settings
from rest_framework import status


def activate_user(request, uid, token):
    """
    View to activate an user
    """
    UserModel = get_user_model()

    try:
        uid = decode_uid(uid)
        user = UserModel.objects.get(pk=uid)

        if not djoser_settings.TOKEN_MODEL.objects.filter(user=user, key=token).exists():
            return HttpResponse("Le lien d'activation est invalide ou a expiré", status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            user.is_active = True
            user.save()
            return HttpResponse("Votre compte a été activé avec succès!", status=status.HTTP_200_OK)
        else:
            return HttpResponse("Ce compte est déjà activé.", status=status.HTTP_400_BAD_REQUEST)

    except UserModel.DoesNotExist:
        return HttpResponse("Utilisateur non trouvé", status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return HttpResponse(f"Erreur d'activation: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
