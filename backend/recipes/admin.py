from django.contrib import admin
from django.utils.translation import gettext as _
from .models import (Favorite, Ingredient, Recipe, RecipeIngredientAmount,
                     ShoppingCart, Tag)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favorites')
    list_filter = ('author', 'name', 'tags',)
    empty_value_display = '-пусто-'

    @staticmethod
    def count_favorites(obj):
        return obj.in_favorites.count()
    count_favorites.short_description = _('Число добавлений в избранноe')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.site_header = 'Административная страница проекта Foodgram'
admin.site.register(Tag)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
admin.site.register(RecipeIngredientAmount)
