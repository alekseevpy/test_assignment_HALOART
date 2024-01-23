"""Админ панель для Списка покупок, продуктов и тегов"""
from django.contrib.admin import ModelAdmin, TabularInline, register, site

from shoping_cart.settings import EMPTY_VALUE_DISPLAY, NUM_SHOW

from .models import Product, ProductShopingCart, ShopingCart, Tag, TagProduct

site.site_header = "Панель администратора"


class TagInline(TabularInline):
    """Класс для отображения Тегов в модели Продуктов"""

    model = TagProduct
    extra = NUM_SHOW


class ProductInline(TabularInline):
    """Класс для отображения Продуктов в модели Списка покупок"""

    model = ProductShopingCart
    extra = NUM_SHOW


@register(ProductShopingCart)
class LinksProdShCAdmin(ModelAdmin):
    pass


@register(TagProduct)
class LinksTagProdAdmin(ModelAdmin):
    pass


@register(Tag)
class TagAdmin(ModelAdmin):
    """Админ панель для Тегов"""

    list_display = (
        "name",
        "slug",
    )
    list_filter = ("name",)


@register(Product)
class ProductAdmin(ModelAdmin):
    """Админ панель для Продуктов"""

    list_display = (
        "name",
        "measurement_unit",
        )
    list_filter = (
        "name",
        "tags__name",
    )
    inlines = (TagInline,)
    save_on_top = True
    empty_value_display = EMPTY_VALUE_DISPLAY


@register(ShopingCart)
class ShopingCartAdmin(ModelAdmin):
    """Админ панель для Списка покупок"""

    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inlines = (ProductInline,)
    save_on_top = True
    empty_value_display = EMPTY_VALUE_DISPLAY
