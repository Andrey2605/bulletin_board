from rest_framework.routers import DefaultRouter

from ads.apps import AdsConfig
from ads.views import AdsViewSet, ReviewViewSet

app_name = AdsConfig.name

router = DefaultRouter()

router.register(r"ads", AdsViewSet, basename="ads")
router.register(r"review", ReviewViewSet, basename="review")

urlpatterns = [] + router.urls
