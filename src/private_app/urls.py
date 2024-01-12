# Third-party imports
from django.urls import include, path
from rest_framework import routers

# Local imports
from . import views

router = routers.DefaultRouter()
router.register(r"studyprogram", views.StudyProgramViewSet, basename="studyprogram")

urlpatterns = [path("", include(router.urls))]
