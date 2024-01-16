# Third-party imports
from django.urls import include, path, re_path
from rest_framework import routers
import djoser
# Local imports
from . import views


# Rename default router info
class PublicAPI(routers.APIRootView):
    """
    Public access to school program information and profiles which allow
    public access.
    """

    pass


class DocumentedPublicRouter(routers.DefaultRouter):
    APIRootView = PublicAPI


router = DocumentedPublicRouter()

router.register(
    r"studyprogram", views.StudyProgramViewSetPublic, basename="studyprogram"
)
router.register(r"school", views.SchoolViewSetPublic, basename="school")
router.register(r"userprofile", views.UserProfileViewSetPublic,
                basename="userprofile")
router.register(r"favorite", views.FavoriteViewSetPublic, basename="favorite")

urlpatterns = [path("", include(router.urls)),
               re_path(r'^auth/', include('djoser.urls')),

               re_path(r'^auth/', include('djoser.urls.jwt')),
               ]
