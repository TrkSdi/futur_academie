from django.contrib.auth import get_user_model
from django.http import HttpResponse
from djoser.utils import decode_uid
from djoser.conf import settings as djoser_settings
from rest_framework import status
from djoser.views import UserViewSet


def activate_user(request, uid, token):
    """
    Vue pour activer un compte utilisateur.
    """
    try:
        uid_decoded = decode_uid(uid)
        user = get_user_model().objects.get(pk=uid_decoded)

        activation_view = UserViewSet.as_view({'post': 'activation'})
        activation_response = activation_view(request, uid=uid, token=token)

        if activation_response.status_code == status.HTTP_204_NO_CONTENT:
            return HttpResponse("Votre compte a été activé avec succès!", status=status.HTTP_200_OK)
        else:
            return HttpResponse("Le lien d'activation est invalide ou a expiré", status=status.HTTP_400_BAD_REQUEST)

    except get_user_model().DoesNotExist:
        return HttpResponse("Utilisateur non trouvé", status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return HttpResponse(f"Erreur d'activation: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
