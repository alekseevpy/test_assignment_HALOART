"""Все основные урл"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, ShopingCartViewSet, TagViewSet

app_name = "api"

router = DefaultRouter()

router.register("products", ProductViewSet, basename="products")
router.register("tags", TagViewSet, basename="tags")
router.register("shoping-cart", ShopingCartViewSet, basename="shoping-cart")


urlpatterns = [
    path("", include(router.urls)),
]
