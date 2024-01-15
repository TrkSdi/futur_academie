# Third-party imports
from django.urls import include, path
from rest_framework import routers

# Local imports
from . import views

router = routers.DefaultRouter()
router.register(
    r"studyprogram", views.StudyProgramViewSetPublic, basename="studyprogram"
)
router.register(r"school", views.SchoolViewSetPublic, basename="school")
router.register(r"userprofile", views.UserProfileViewSetPublic, basename="userprofile")
router.register(r"favorite", views.FavoriteViewSetPublic, basename="favorite")

urlpatterns = [path("", include(router.urls))]
