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
from gen.viewsets.books import BookViewSet

from gen.views.shop import shop_detail
from gen.views.generate_shop import generate_shop

router = routers.SimpleRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"system", SystemViewSet, basename="system")
router.register(r"item", ItemViewSet, basename="item")
router.register(r"spell", SpellViewSet, basename="spell")
router.register(r"shop", ShopViewSet, basename="shop")
router.register(r"job", JobViewSet, basename="job")
router.register(r"book", BookViewSet, basename="book")


urlpatterns = [
    path("api/v1/", include(router.urls)),
    # Optional UI:
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("shop/<id>", shop_detail, name="shop_detail"),
    path("generate/shop", generate_shop, name="generate_shop"),
    # Healthcheck
    path(r"ht/", include("health_check.urls")),
]
