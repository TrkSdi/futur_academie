# Third-party imports
from django.urls import include, path
from rest_framework import routers

# Local imports
from . import views

router = routers.DefaultRouter()
router.register(r"studyprogram", views.StudyProgramViewSet, basename="studyprogram")
router.register(r"school", views.SchoolViewSet, basename="school")
router.register(r"userprofile", views.UserProfileViewSet, basename="userprofile")
router.register(r"favorite", views.FavoriteViewSet, basename="favorite")

urlpatterns = [path("", include(router.urls))]
