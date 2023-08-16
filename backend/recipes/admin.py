from django.contrib import admin


from recipes.models import (Favorite,
                            Ingredient,
                            Recipe,
                            RecipeIngredientAmount,
                            ShoppingCart,
                            Tag)
from recipes.validate_delete import ValidateDeliteForm


class TagStackedInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 0
    min_num = 1
    formset = ValidateDeliteForm


class RecipeIngredientAmountInline(admin.TabularInline):
    model = RecipeIngredientAmount
    extra = 0
    min_num = 1
    formset = ValidateDeliteForm


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',)
    list_filter = ('author', 'name', 'tags',)
    empty_value_display = '-пусто-'
    inlines = [TagStackedInline, RecipeIngredientAmountInline]
    exclude = ('tags',)
    formset = ValidateDeliteForm


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = ('user', 'recipe', )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    model = ShoppingCart
    list_display = ('user', 'recipe', )


admin.site.site_header = 'Административная страница проекта Foodgram'
admin.site.register(RecipeIngredientAmount)
