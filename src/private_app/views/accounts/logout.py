from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response


class LogoutAPIView(APIView):
    permission_classes = [AllowAny]
    """logout view that blacklists the refresh token when the user logs out
    """

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'detail': 'Déconnexion réussie.'}, status=200)
            except Exception as e:
                return Response({'detail': str(e)}, status=400)
        else:
            return Response({'detail': "Le paramètre Token 'refresh' est manquant."}, status=400)
