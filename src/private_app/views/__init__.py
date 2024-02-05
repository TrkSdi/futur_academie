from .link import LinkSerializer
from .school import SchoolSerializer, SchoolReducedSerializer, SchoolViewSet
from .studyprogram import (
    StudyProgramSerializer,
    StudyProgramViewSet,
    StudyProgramReducedSerializer,
)

from .favorite import FavoriteSerializer, FavoriteViewSet

from .userprofile import UserProfileSerializer, UserSerializer, UserProfileViewSet

from .address import AddressSerializer, AddressViewSet


from .accounts.logout import LogoutAPIView
from .accounts.activation import ActivateUser

# not currently used, trying to fix axes problem with this
# from .lockout import lockout
