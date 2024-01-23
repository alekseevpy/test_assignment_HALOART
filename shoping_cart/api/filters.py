"""Фильтр для Продуктов, Списка покупок"""
import django_filters as filters
from products.models import Product, Tag
from rest_framework.filters import SearchFilter


class ProductSearchFilter(SearchFilter):
    """Поиск по названию Продукта"""

    search_param = "name"


class ProductFilter(filters.FilterSet):
    """Фильтр для Продукта"""

    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Product
        fields = ("tags",)
