from django.urls import include
from django.urls import path
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from gen.viewsets.users import UserViewSet
from gen.viewsets.systems import SystemViewSet
from gen.viewsets.items import ItemViewSet
from gen.viewsets.spells import SpellViewSet
from gen.viewsets.shops import ShopViewSet
from gen.viewsets.jobs import JobViewSet

router = routers.SimpleRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"system", SystemViewSet, basename="system")
router.register(r"item", ItemViewSet, basename="item")
router.register(r"spell", SpellViewSet, basename="spell")
router.register(r"shop", ShopViewSet, basename="shop")
router.register(r"job", JobViewSet, basename="job")


urlpatterns = [
    path("api/v1/", include(router.urls)),
    # Optional UI:
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
