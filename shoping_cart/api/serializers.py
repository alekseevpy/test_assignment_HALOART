from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import transaction
from products.models import Product, ProductShopingCart, ShopingCart, Tag
from rest_framework import serializers

from shoping_cart.settings import MAX_AMOUNT, MIN_AMOUNT


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения Тега или Списка тегов"""

    class Meta:
        model = Tag
        fields = ("id", "name", "slug")


class ProductSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения Продукта или Списка продуктов"""

    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        fields = ("id", "name", "measurement_unit", "tags")

    def create(self, validated_data):
        """Создание Продукта"""
        tags_data = validated_data.pop("tags", [])
        product = Product.objects.create(**validated_data)

        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            product.tags.add(tag)

        return product

    def update(self, instance, validated_data):
        """Изменение Продукта"""
        tags_data = validated_data.pop("tags", [])
        instance.tags.clear()

        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            instance.tags.add(tag)

        instance.name = validated_data.get("name", instance.name)
        instance.measurement_unit = validated_data.get(
            "measurement_unit", instance.measurement_unit
        )
        instance.save()

        return instance


class ProductInShopingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения Продуктов в Списке покупок"""

    id = serializers.IntegerField(
        source="product.id",
    )
    name = serializers.ReadOnlyField(
        source="product.name",
    )
    measurement_unit = serializers.ReadOnlyField(
        source="product.measurement_unit",
    )
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = ProductShopingCart
        fields = ("id", "name", "measurement_unit", "amount", "tags")


class AddProductToShopingCartSerializer(serializers.ModelSerializer):
    """Сериалайзер для добавления Продукта в Список покупок"""

    id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    amount = serializers.IntegerField(
        write_only=True,
        validators=(
            MinValueValidator(
                MIN_AMOUNT, "Количество ингредиента не должно быть меньше 1."
            ),
            MaxValueValidator(
                MAX_AMOUNT,
                ("Вы указали слишком большое количество ингредиента"),
            ),
        ),
    )

    class Meta:
        model = ProductShopingCart
        fields = ("id", "amount")


class GetShopingCartSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения Списка покупок или Списков покупок"""

    products = serializers.SerializerMethodField()

    class Meta:
        model = ShopingCart
        fields = (
            "id",
            "name",
            "products",
        )

    def get_products(self, obj):
        products = ProductShopingCart.objects.filter(shoping_cart=obj)
        return ProductInShopingCartSerializer(products, many=True).data


class CreateShopingCartSerializer(GetShopingCartSerializer):
    """Сериализатор для создания, удаления и обновления Списка покупок"""

    products = AddProductToShopingCartSerializer(many=True)

    class Meta:
        model = ShopingCart
        fields = (
            "id",
            "name",
            "products",
        )

    def validate(self, data):
        """Проверка данных при создании/редактировании Списка покупок"""
        request = self.context.get("request")
        name = data.get("name")
        if (
            request.method == "POST"
            and ShopingCart.objects.filter(name=name).exists()
        ):
            raise ValidationError(
                "Список покупок с таким именем уже существует!"
            )

        products = data["products"]
        if not products:
            raise ValidationError("Необходим хотя бы один продукт!")
        prod_list = []
        for product in products:
            prod_id = product["id"]
            if prod_id in prod_list:
                raise ValidationError("Выберите различные продукты!")
            prod_list.append(prod_id)
        return data

    def create_products(self, products, shoping_cart):
        """Функция добавления Списка продуктов в Список покупок"""
        ProductShopingCart.objects.bulk_create(
            [
                ProductShopingCart(
                    product=product["id"],
                    shoping_cart=shoping_cart,
                    amount=product["amount"],
                )
                for product in products
            ]
        )

    @transaction.atomic
    def create(self, validated_data):
        """Создание Списка покупок"""
        products = validated_data.pop("products")
        shoping_cart = ShopingCart.objects.create(**validated_data)
        self.create_products(products, shoping_cart)
        shoping_cart.save()
        return shoping_cart

    @transaction.atomic
    def update(self, instance, validated_data):
        """Обновление Списка покупок"""
        instance.name = validated_data.pop("name", instance.name)
        products = validated_data.pop("products")
        ProductShopingCart.objects.filter(shoping_cart=instance).delete()
        self.create_products(products, instance)
        return super().update(instance, validated_data)

    def represente(self, instance):
        """Отображение Списка покупок"""
        serializer = GetShopingCartSerializer(
            instance, context={"request": self.context.get("request")}
        )
        return serializer.data
