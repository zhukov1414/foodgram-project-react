from django.contrib import admin
from django.utils.translation import gettext as _


from recipes.models import (Favorite, Ingredient, Recipe,
                            RecipeIngredientAmount, ShoppingCart, Tag)


class TagStackedInline(admin.StackedInline):
    model = Recipe.tags.through
    extra = 1


class RecipeIngredientAmountInline(admin.TabularInline):
    model = RecipeIngredientAmount
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favorites')
    list_filter = ('author', 'name', 'tags',)
    empty_value_display = '-пусто-'
    inlines = [TagStackedInline, RecipeIngredientAmountInline]

    @staticmethod
    def count_favorites(obj):
        return obj.in_favorites.count()
    count_favorites.short_description = _('Число добавлений в избранное')

    def save_model(self, request, obj, form, change):
        if not obj.ingredients.exists():
            raise admin.ValidationError(_('Добавь минимум один ингредиент'))
        super().save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.site_header = 'Административная страница проекта Foodgram'
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
admin.site.register(RecipeIngredientAmount)
