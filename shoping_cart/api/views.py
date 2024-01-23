from django_filters.rest_framework import DjangoFilterBackend
from products.models import Product, ShopingCart, Tag
from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilter, ProductSearchFilter
from .paginators import PageLimitPagination
from .serializers import (
    CreateShopingCartSerializer,
    GetShopingCartSerializer,
    ProductSerializer,
    TagSerializer,
)


class TagViewSet(ModelViewSet):
    """Получение Тега или списка всех Тегов"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PageLimitPagination


class ProductViewSet(ModelViewSet):
    """
    Получение Продукта или списка всех Продуктов,
    поиск по частичному вхождению в начале названия Продукта.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, ProductSearchFilter)
    filterset_class = ProductFilter
    pagination_class = PageLimitPagination
    search_fields = ("^name",)

    def get_queryset(self):
        queryset = super().get_queryset()
        # Добавление сортировки
        sort_param = self.request.query_params.get("sort", None)
        if sort_param == "measurement_unit":
            queryset = queryset.order_by("measurement_unit")
        elif sort_param == "name":
            queryset = queryset.order_by("name")
        return queryset


class ShopingCartViewSet(ModelViewSet):
    """
    Получение, создание и частичное изменение, а так же
    удаления Списка покупок.
    """

    queryset = ShopingCart.objects.all()
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = ProductFilter
    pagination_class = PageLimitPagination

    def get_serializer_class(self):
        method = self.request.method
        if method == "POST" or method == "PATCH":
            return CreateShopingCartSerializer
        return GetShopingCartSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
