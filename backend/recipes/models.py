import re
from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from foodgram.settings import MAX_LENGTH


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=MAX_LENGTH,
                            verbose_name='Название ингридиента'
                            )
    measurement_unit = models.CharField(max_length=16,
                                        verbose_name='Единица измерения'
                                        )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название тега',
        unique=True
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг тега'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
    
    def clean(self):
        hex_color_pattern = r'^#(?:[0-9a-fA-F]{3}){1,2}$'
        if not re.match(hex_color_pattern, self.color):
            raise ValidationError('Цвет должен быть в формате hex-цвета (#RRGGBB)')


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes'
    )
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/images',
        blank=True,
        null=True,
        verbose_name='Изображение рецепта'
    )
    text = models.TextField(
        verbose_name='Текстовое описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientAmount',
        verbose_name='Ингредиенты',
        related_name="recipes",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время публикации'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipes'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        null=True
    )

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='recipe_ingredient_unique')]

    def __str__(self):
        return self.ingredient.name


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт в списке покупок',
        related_name='in_shopping_carts'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец списка покупок',
        related_name='shopping_carts'
    )
    added_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        ordering = ['-added_date']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='shopping_cart_recipe_unique')]

    def __str__(self):
        return f'{self.user}:{self.recipe}'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт в списке избранных',
        related_name='in_favorites'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites'
    )
    added_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления в список избранного'
    )

    class Meta:
        ordering = ['-added_date']
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Списки избранного'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='favorite_recipe_unique')]

    def __str__(self):
        return f'{self.user}:{self.recipe}'
