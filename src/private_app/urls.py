# Third-party imports
from django.urls import include, path
from rest_framework import routers

# Local imports
from . import views


# Rename default router info
class PrivateAPI(routers.APIRootView):
    """
    Public access to school program information which allows admins to edit it
    and crud access to the profile and favorites of an authenticated user.
    """

    pass


class DocumentedPrivateRouter(routers.DefaultRouter):
    APIRootView = PrivateAPI


router = DocumentedPrivateRouter()

router.register(r"studyprogram", views.StudyProgramViewSet, basename="studyprogram")
router.register(r"school", views.SchoolViewSet, basename="school")
router.register(r"userprofile", views.UserProfileViewSet, basename="userprofile")
router.register(r"favorite", views.FavoriteViewSet, basename="favorite")

urlpatterns = [path("", include(router.urls))]
