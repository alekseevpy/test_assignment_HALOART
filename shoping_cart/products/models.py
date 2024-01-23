from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from shoping_cart.settings import MAX_AMOUNT, MIN_AMOUNT


class Tag(models.Model):
    """Модель Тегов"""

    name = models.CharField(
        verbose_name="Тег",
        max_length=200,
        unique=False,
    )
    slug = models.SlugField(
        verbose_name="Уникальный слаг",
        max_length=200,
        unique=False,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    """Модель для продуктов"""

    name = models.CharField(
        verbose_name="Наименование",
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name="Единица измерения",
        max_length=200,
    )
    tags = models.ManyToManyField(
        Tag,
        through="TagProduct",
        related_name="products",
    )

    class Meta:
        """Проверка полей"""

        ordering = ("name",)
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name}, измеряется в: {self.measurement_unit}"


class ShopingCart(models.Model):
    """Модель списка покупок"""

    name = models.CharField(
        verbose_name="Название списка покупок. Пример: Перекресток 27.01.24",
        max_length=70,
    )
    products = models.ManyToManyField(
        Product,
        through="ProductShopingCart",
        related_name="recipes",
    )

    class Meta:
        """Проверка полей"""

        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"

    def __str__(self):
        return f"{self.name}"


class TagProduct(models.Model):
    """Модель для связи Тега и Продукта"""

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Тег")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Продукт",
    )

    class Meta:
        """Проверка полей"""

        verbose_name = "Тег продукта"
        verbose_name_plural = "Теги продукта"
        constraints = (
            models.UniqueConstraint(
                fields=("product", "tag"), name="unique_product_tag"
            ),
        )

    def __str__(self):
        return f"Продукт: {self.product.name} содержит тег: {self.tag}"


class ProductShopingCart(models.Model):
    """Модель для связи Продукта и Списка покупок"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="amount",
        verbose_name="Продукт",
    )
    shoping_cart = models.ForeignKey(
        ShopingCart,
        on_delete=models.CASCADE,
        related_name="product",
        verbose_name="Список покупок",
    )
    amount = models.PositiveSmallIntegerField(
        "Количество",
        validators=(
            MinValueValidator(
                MIN_AMOUNT, "Количество ингредиента не должно быть меньше 1."
            ),
            MaxValueValidator(
                MAX_AMOUNT,
                ("Указано слишком большое количество ингредиента"),
            ),
        ),
    )

    class Meta:
        """Проверка полей"""

        ordering = ("shoping_cart",)
        verbose_name = "Продукт"
        verbose_name_plural = "Количество продуктов"
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "shoping_cart",
                    "product",
                ),
                name="unique_product_in_shoping_cart",
            ),
        )

    def __str__(self):
        return f"{self.shoping_cart.name} " f"содержит {self.product.name}"
